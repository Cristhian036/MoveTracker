from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
import cv2
import time
import numpy as np
from ultralytics import YOLO
import supervision as sv
import os
# import pytesseract # Removed Tesseract
from django.core.files.storage import FileSystemStorage
import sys
from parking.models import ParkingReservation, ParkingSpace, Vehicle, ParkingAssignment, VehicleType
from django.utils import timezone
from django.contrib.auth import get_user_model

# Importar motor OCR personalizado
try:
    from .ocr import read_plate_text
except ImportError:
    print("Error: No se pudo importar el motor OCR desde detection.ocr")
    def read_plate_text(img): return []

import re

# Configuracion
BASE_DIR = settings.BASE_DIR
MODEL_VEHICLE_PATH = os.path.join(BASE_DIR, 'detection', 'models', 'yolov10n.pt')
MODEL_PLATE_PATH = os.path.join(BASE_DIR, 'detection', 'models', 'best.pt') # Updated to best.pt
VIDEO_PATH = os.path.join(BASE_DIR, 'detection', 'videos')
# TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe' # Removed Tesseract

# Configurar comando tesseract
# try:
#     pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
# except:
#     pass

# Diccionario global para ultimas detecciones
latest_detections = {}
# Diccionario global para historial de detecciones
detection_history = {}
# Diccionario global para progreso de video
video_progress = {}
# Diccionario global para estado de rastreo (indice actual en historial)
tracking_state = {}
# Diccionario global para contador de frames sin placa
frames_without_plate_state = {}
# Diccionario global para estado del video
video_status = {}

def create_automatic_reservation(plate, vehicle_type_str, user):
    # Map vehicle type
    type_map = {
        'car': VehicleType.CAR,
        'truck': VehicleType.TRUCK,
        'motorcycle': VehicleType.MOTORCYCLE,
        'bus': VehicleType.TRUCK,
        'Auto': VehicleType.CAR,
        'Camioneta': VehicleType.TRUCK,
        'Moto': VehicleType.MOTORCYCLE
    }
    v_type = type_map.get(vehicle_type_str, VehicleType.CAR)
    
    # Check if vehicle is already inside (active assignment)
    active_assignment = ParkingAssignment.objects.filter(
        vehicle__license_plate=plate,
        status=ParkingAssignment.AssignmentStatus.ACTIVE
    ).exists()
    
    if active_assignment:
        return False

    # Find available space
    space = ParkingSpace.objects.filter(
        status=ParkingSpace.SpaceStatus.AVAILABLE,
        is_active=True
    ).first()
    
    if not space:
        return False
        
    try:
        # Get or create vehicle
        vehicle, created = Vehicle.objects.get_or_create(
            license_plate=plate,
            defaults={
                'vehicle_type': v_type,
                'color': 'Desconocido',
                'owner': None,
                'registered_by': user if user and user.is_authenticated else None
            }
        )
        
        if not created and not vehicle.vehicle_type:
            vehicle.vehicle_type = v_type
            vehicle.save()
            
        # Create Reservation
        reservation = ParkingReservation(
            customer_name="Cliente Rápido (Cámara)",
            vehicle_plate=plate,
            vehicle_type_temp=v_type,
            parking_space=space,
            reservation_date=timezone.now(),
            status=ParkingReservation.ReservationStatus.CONFIRMED,
            is_quick_reservation=True,
            created_by=user if user and user.is_authenticated else None,
            vehicle=vehicle
        )
        reservation.save()
        
        # Create Assignment
        assignment = ParkingAssignment(
            vehicle=vehicle,
            parking_space=space,
            status=ParkingAssignment.AssignmentStatus.ACTIVE,
            assigned_by=user if user and user.is_authenticated else None,
            entry_time=timezone.now()
        )
        assignment.save()
        
        # Update Space
        space.status = ParkingSpace.SpaceStatus.OCCUPIED
        space.save()
        
        return True
        
    except Exception as e:
        print(f"Error creating automatic reservation: {e}")
        return False

def cropped(detections, image):
    bounding_box = detections.xyxy
    if len(bounding_box) == 0:
        return None
    xmin, ymin, xmax, ymax = bounding_box[0]
    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
    # Asegurar coordenadas dentro de imagen
    h, w, _ = image.shape
    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(w, xmax)
    ymax = min(h, ymax)
    
    if xmin >= xmax or ymin >= ymax:
        return None
        
    cropped_image = image[ymin:ymax, xmin:xmax]
    return cropped_image

def stream_video(source=VIDEO_PATH, detection_id=None, delete_source=False, start_frame=0, user=None):
    if isinstance(source, int):
        # Usar DirectShow para camara en Windows
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(source)
        if start_frame > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
    if not cap.isOpened():
        print(f'Error: No se puede abrir la fuente de video: {source}')
        # Intentar camara alternativa si falla
        if isinstance(source, int):
             print(f'Intentando abrir camara {source} sin CAP_DSHOW...')
             cap = cv2.VideoCapture(source)
             if not cap.isOpened():
                 return
        else:
            return

    model_t = YOLO(MODEL_VEHICLE_PATH)
    model_p = YOLO(MODEL_PLATE_PATH)
    
    bounding_box_annotator_vehicle = sv.BoundingBoxAnnotator(color=sv.Color.GREEN, thickness=3)
    label_annotator_vehicle = sv.LabelAnnotator(color=sv.Color.GREEN, text_thickness=2, text_scale=0.8)
    
    bounding_box_annotator_plate = sv.BoundingBoxAnnotator(color=sv.Color.RED, thickness=4)
    label_annotator_plate = sv.LabelAnnotator(color=sv.Color.RED, text_thickness=2, text_scale=1.0)

    # Calcular delay para mantener FPS original (solo videos)
    delay = 0
    if not isinstance(source, int):
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            delay = 1 / fps

    if start_frame == 0 and detection_id:
        # Resetear historial y estados si se inicia desde el principio
        detection_history[detection_id] = []
        latest_detections[detection_id] = {}
        video_progress[detection_id] = 0
        tracking_state.pop(detection_id, None)
        frames_without_plate_state.pop(detection_id, None)
        video_status[detection_id] = 'playing'

    # Recuperar estado previo si existe
    frames_without_plate = frames_without_plate_state.get(detection_id, 0) if detection_id else 0
    current_history_index = tracking_state.get(detection_id) if detection_id else None

    try:
        while cap.isOpened():
            start_time = time.time()
            
            # Actualizar progreso
            if detection_id:
                video_progress[detection_id] = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            ret, frame = cap.read()
            if not ret:
                if isinstance(source, str):
                    if detection_id:
                        video_status[detection_id] = 'finished'
                    break
                else:
                    print("Error: Failed to capture frame from live camera.")
                    break

            results_t = model_t(frame, verbose=False)[0]
            detections_t = sv.Detections.from_ultralytics(results_t)

            class_id = [2, 3, 5, 7] # car, motorcycle, bus, truck
            
            # Filtrar detecciones
            mask = np.isin(detections_t.class_id, class_id)
            detections_t = detections_t[mask]

            annotated_image = frame.copy()
            plate_detected_in_frame = False

            if len(detections_t) > 0:
                # Seleccionar solo el vehiculo mas cercano (mayor area)
                areas = (detections_t.xyxy[:, 2] - detections_t.xyxy[:, 0]) * (detections_t.xyxy[:, 3] - detections_t.xyxy[:, 1])
                max_area_index = np.argmax(areas)
                detections_t = detections_t[[max_area_index]]
                
                # Obtener tipo de vehiculo
                vehicle_class_id = detections_t.class_id[0]
                vehicle_type = model_t.names[vehicle_class_id]
                
                # Reemplazar 'bus' por 'truck' si se solicita
                if vehicle_type == 'bus':
                    vehicle_type = 'truck'
                
                # Traducir a español
                translations = {
                    'car': 'Auto',
                    'truck': 'Camioneta',
                    'motorcycle': 'Moto'
                }
                vehicle_type = translations.get(vehicle_type, vehicle_type)

                # Anotar vehiculos
                annotated_image = bounding_box_annotator_vehicle.annotate(scene=annotated_image, detections=detections_t)
                annotated_image = label_annotator_vehicle.annotate(scene=annotated_image, detections=detections_t, labels=[vehicle_type])
                
                # Procesar primer vehiculo para placa
                cropped_image_t = cropped(detections_t, frame)
                
                if cropped_image_t is not None and cropped_image_t.size > 0:
                    results_p = model_p(cropped_image_t, agnostic_nms=True, verbose=False)[0]
                    results_p.names[0] = 'Matricula'
                    detections_p = sv.Detections.from_ultralytics(results_p)
                    
                    if len(detections_p) > 0:
                        # Recortar placa para OCR antes de modificar coordenadas
                        cropped_image_matricula = cropped(detections_p, cropped_image_t)

                        # Calcular nuevas coordenadas de placa
                        # Usamos detections_p.xyxy que ya es numpy array (CPU) en lugar de results_p.boxes (GPU)
                        width = detections_p.xyxy[0][2] - detections_p.xyxy[0][0]
                        height = detections_p.xyxy[0][3] - detections_p.xyxy[0][1]
                        
                        x1_nuevo = detections_t.xyxy[0][0] + detections_p.xyxy[0][0]
                        y1_nuevo = detections_t.xyxy[0][1] + detections_p.xyxy[0][1]
                        x2_nuevo = x1_nuevo + width
                        y2_nuevo = y1_nuevo + height
                        
                        detections_p.xyxy = np.array([[x1_nuevo, y1_nuevo, x2_nuevo, y2_nuevo]])
                        
                        # Anotar placa
                        annotated_image = bounding_box_annotator_plate.annotate(scene=annotated_image, detections=detections_p)
                        # Forzar etiqueta "Matricula"
                        labels_p = ["Matricula"] * len(detections_p)
                        annotated_image = label_annotator_plate.annotate(scene=annotated_image, detections=detections_p, labels=labels_p)
                        
                        # Reconocimiento optico de caracteres (NUEVO MOTOR EASYOCR)
                        if cropped_image_matricula is not None and cropped_image_matricula.size > 0:
                            try:
                                # Usar el nuevo motor OCR (EasyOCR)
                                # read_plate_text ya incluye preprocesamiento (zoom, threshold)
                                ocr_results = read_plate_text(cropped_image_matricula)
                                
                                # Procesar resultados
                                best_text = ""
                                best_conf = 0.0
                                
                                for (bbox, text, prob) in ocr_results:
                                    # Limpieza basica
                                    clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                                    
                                    # Validar longitud minima (placas Peru suelen ser 6 caracteres)
                                    if len(clean_text) >= 5 and prob > best_conf:
                                        best_text = clean_text
                                        best_conf = prob
                                
                                if best_text:
                                    plate_detected_in_frame = True
                                    # Formatear para mostrar (ej. ABC-123)
                                    display_text = best_text
                                    if len(best_text) == 6:
                                        display_text = f"{best_text[:3]}-{best_text[3:]}"
                                        
                                    # Dibujar texto en cuadro
                                    cv2.putText(annotated_image, f'Plate: {display_text} ({best_conf:.2f})', (int(x1_nuevo), int(y1_nuevo)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                                    
                                    # Actualizar ultima deteccion SOLO si la confianza es mayor
                                    if detection_id:
                                        previous_data = latest_detections.get(detection_id, {})
                                        previous_conf = previous_data.get('confidence', 0.0)
                                        
                                        if best_conf > previous_conf:
                                            latest_detections[detection_id] = {
                                                'plate': display_text,
                                                'vehicle_type': vehicle_type,
                                                'confidence': best_conf
                                            }
                                        
                                        # Actualizar historial de detecciones
                                        if detection_id not in detection_history:
                                            detection_history[detection_id] = []
                                        
                                        history_list = detection_history[detection_id]
                                        
                                        # Si no estamos rastreando un vehiculo especifico (current_history_index es None),
                                        # asumimos que es un nuevo vehiculo y creamos una nueva entrada.
                                        if current_history_index is None:
                                            history_list.append({
                                                'plate': display_text,
                                                'vehicle_type': vehicle_type,
                                                'confidence': best_conf,
                                                'registered': False
                                            })
                                            current_history_index = len(history_list) - 1
                                            if detection_id:
                                                tracking_state[detection_id] = current_history_index
                                            
                                            # Limitar historial a ultimos 50 registros
                                            if len(history_list) > 50:
                                                history_list.pop(0)
                                                current_history_index -= 1 # Ajustar indice si se elimino el primero
                                                if detection_id:
                                                    tracking_state[detection_id] = current_history_index
                                        else:
                                            # Si estamos rastreando un vehiculo, actualizamos su entrada si la confianza es mejor
                                            # o si simplemente queremos mantener la ultima lectura mas confiable
                                            if current_history_index < len(history_list):
                                                current_entry = history_list[current_history_index]
                                                # Actualizar solo si la confianza es mayor para obtener la mejor lectura posible de este vehiculo
                                                if best_conf > current_entry['confidence']:
                                                    current_entry['plate'] = display_text
                                                    current_entry['vehicle_type'] = vehicle_type
                                                    current_entry['confidence'] = best_conf
                                        
                                        # Intentar registrar reserva automatica si es camara en vivo y confianza alta
                                        if current_history_index is not None and current_history_index < len(history_list):
                                            current_entry = history_list[current_history_index]
                                            if (not current_entry.get('registered', False) and 
                                                current_entry['confidence'] > 0.85 and 
                                                detection_id and detection_id.startswith('live_')):
                                                
                                                success = create_automatic_reservation(current_entry['plate'], current_entry['vehicle_type'], user)
                                                if success:
                                                    current_entry['registered'] = True
                                                    # Opcional: Agregar indicador visual en la imagen
                                                    cv2.putText(annotated_image, 'REGISTRADO', (int(x1_nuevo), int(y1_nuevo)-40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                            except Exception as e:
                                print(f'OCR Error: {e}')
                                pass

            # Resetear confianza si no se detecta placa por un tiempo (ej. 30 frames)
            if not plate_detected_in_frame:
                frames_without_plate += 1
            else:
                frames_without_plate = 0
            
            # Guardar estado de frames sin placa
            if detection_id:
                frames_without_plate_state[detection_id] = frames_without_plate
            
            if frames_without_plate > 30 and detection_id:
                # Resetear rastreo de vehiculo actual en historial
                current_history_index = None
                tracking_state.pop(detection_id, None)
                
                if detection_id in latest_detections:
                    # Resetear confianza para permitir nuevas detecciones de otros vehiculos
                    latest_detections[detection_id]['confidence'] = 0.0

            # Redimensionar para visualizacion
            # frame_display = cv2.resize(annotated_image, (1280, 720))
            
            # Usar cuadro original para respetar aspecto
            frame_display = annotated_image

            _, jpeg = cv2.imencode('.jpg', frame_display)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
            
            # Controlar velocidad de reproduccion
            if delay > 0:
                elapsed = time.time() - start_time
                wait = delay - elapsed
                if wait > 0:
                    time.sleep(wait)

    finally:
        cap.release()
        if delete_source and isinstance(source, str) and os.path.exists(source):
            try:
                os.remove(source)
            except Exception as e:
                print(f"Error deleting file {source}: {e}")

def video_feed(request):
    return StreamingHttpResponse(stream_video(VIDEO_PATH, detection_id='default_video'), content_type='multipart/x-mixed-replace; boundary=frame')

def live_feed(request):
    camera_index = request.GET.get('camera_index', '0')
    try:
        camera_index = int(camera_index)
    except ValueError:
        camera_index = 0
    return StreamingHttpResponse(stream_video(camera_index, detection_id=f'live_{camera_index}', user=request.user), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return redirect('/')

def live_camera(request):
    return render(request, 'detection/live_camera.html')

import base64

@ensure_csrf_cookie
def upload_video(request):
    if request.method == 'POST':
        # Opcion 1: Subida de archivo (Prioridad)
        if request.FILES.get('video_file'):
            video_file = request.FILES['video_file']
            fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media', 'videos'))
            filename = fs.save(video_file.name, video_file)
            return render(request, 'detection/upload_video.html', {
                'uploaded_video_url': filename,
                'video_name': video_file.name
            })
        
        # Opcion 2: Ruta local (Legacy)
        video_path = request.POST.get('video_path')
        if video_path:
            # Limpiar comillas si el usuario copio como ruta
            video_path = video_path.strip('"').strip("'")
            
            if os.path.exists(video_path):
                # Codificar ruta para pasarla en URL de forma segura
                encoded_path = base64.urlsafe_b64encode(video_path.encode()).decode()
                return render(request, 'detection/upload_video.html', {
                    'uploaded_video_url': encoded_path,
                    'video_name': os.path.basename(video_path)
                })
            else:
                return render(request, 'detection/upload_video.html', {'error': 'El archivo no existe en la ruta especificada.'})
            
    return render(request, 'detection/upload_video.html')

def uploaded_video_feed(request, filename):
    video_path = None
    should_delete = False
    
    # Intentar decodificar como ruta local (base64)
    try:
        decoded_path = base64.urlsafe_b64decode(filename).decode()
        if os.path.exists(decoded_path):
            video_path = decoded_path
            should_delete = False
    except Exception:
        pass
    
    # Si no es ruta local, buscar en media/videos (es un archivo subido)
    if not video_path:
        video_path = os.path.join(BASE_DIR, 'media', 'videos', filename)
        should_delete = False # No borrar automaticamente para permitir reinicio

    try:
        start_frame = int(request.GET.get('start_frame', 0))
    except ValueError:
        start_frame = 0
        
    # delete_source=True si es un archivo subido, False si es ruta local
    return StreamingHttpResponse(stream_video(video_path, detection_id=f'upload_{filename}', delete_source=should_delete, start_frame=start_frame), content_type='multipart/x-mixed-replace; boundary=frame')

def get_latest_plate(request):
    detection_id = request.GET.get('detection_id')
    detection_data = latest_detections.get(detection_id, {})
    history = detection_history.get(detection_id, [])
    current_frame = video_progress.get(detection_id, 0)
    status = video_status.get(detection_id, 'playing')
    
    if isinstance(detection_data, str):
        return JsonResponse({'plate': detection_data, 'vehicle_type': '', 'current_frame': current_frame, 'history': [], 'status': status})
        
    return JsonResponse({
        'plate': detection_data.get('plate', ''),
        'vehicle_type': detection_data.get('vehicle_type', ''),
        'confidence': detection_data.get('confidence', 0.0),
        'current_frame': current_frame,
        'history': history,
        'status': status
    })

def delete_video(request, filename):
    # Intentar decodificar como ruta local (base64)
    try:
        decoded_path = base64.urlsafe_b64decode(filename).decode()
        if os.path.exists(decoded_path):
            # Es ruta local, no borrar
            return JsonResponse({'status': 'ignored'})
    except Exception:
        pass
    
    # Es archivo subido
    file_path = os.path.join(BASE_DIR, 'media', 'videos', filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return JsonResponse({'status': 'deleted'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'not_found'})
