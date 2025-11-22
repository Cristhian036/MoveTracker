from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import os
import pytesseract
from django.core.files.storage import FileSystemStorage

# Configuracion
BASE_DIR = settings.BASE_DIR
MODEL_VEHICLE_PATH = os.path.join(BASE_DIR, 'detection', 'models', 'yolov10n.pt')
MODEL_PLATE_PATH = os.path.join(BASE_DIR, 'detection', 'models', 'placa.pt')
VIDEO_PATH = os.path.join(BASE_DIR, 'detection', 'videos', 'video.mp4')
TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Configurar comando tesseract
try:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
except:
    pass

# Diccionario global para ultimas detecciones
latest_detections = {}

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

def stream_video(source=VIDEO_PATH, detection_id=None):
    if isinstance(source, int):
        # Usar DirectShow para camara en Windows
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(source)
        
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

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                if isinstance(source, str):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
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

            if len(detections_t) > 0:
                # Anotar vehiculos
                annotated_image = bounding_box_annotator_vehicle.annotate(scene=annotated_image, detections=detections_t)
                annotated_image = label_annotator_vehicle.annotate(scene=annotated_image, detections=detections_t)
                
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
                        dif_x = results_p.boxes.xyxy[0][2] - results_p.boxes.xyxy[0][0]
                        dif_y = results_p.boxes.xyxy[0][3] - results_p.boxes.xyxy[0][1]
                        
                        x1_nuevo = detections_t.xyxy[0][0] + detections_p.xyxy[0][0]
                        y1_nuevo = detections_t.xyxy[0][1] + detections_p.xyxy[0][1]
                        x2_nuevo = x1_nuevo + dif_x
                        y2_nuevo = y1_nuevo + dif_y
                        
                        detections_p.xyxy = np.array([[x1_nuevo, y1_nuevo, x2_nuevo, y2_nuevo]])
                        
                        # Anotar placa
                        annotated_image = bounding_box_annotator_plate.annotate(scene=annotated_image, detections=detections_p)
                        annotated_image = label_annotator_plate.annotate(scene=annotated_image, detections=detections_p)
                        
                        # Reconocimiento optico de caracteres
                        if cropped_image_matricula is not None and cropped_image_matricula.size > 0:
                            try:
                                gray = cv2.cvtColor(cropped_image_matricula, cv2.COLOR_BGR2GRAY)
                                data = pytesseract.image_to_string(gray, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYXabcdefghijklmnopqrstuvwxyz')
                                
                                valor_medio = round(len(data)/2)
                                # Limpieza simple basada en script original
                                if len(data) > 6:
                                    data = data[max(0, valor_medio-3):min(len(data), valor_medio+4)]
                                
                                # Dibujar texto en cuadro
                                cv2.putText(annotated_image, f'Plate: {data.strip()}', (int(x1_nuevo), int(y1_nuevo)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                                
                                # Actualizar ultima deteccion
                                if detection_id and data.strip():
                                    latest_detections[detection_id] = data.strip()
                                
                            except Exception as e:
                                print(f'OCR Error: {e}')
                                pass

            # Redimensionar para visualizacion
            # frame_display = cv2.resize(annotated_image, (1280, 720))
            
            # Usar cuadro original para respetar aspecto
            frame_display = annotated_image

            _, jpeg = cv2.imencode('.jpg', frame_display)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    finally:
        cap.release()

def video_feed(request):
    return StreamingHttpResponse(stream_video(VIDEO_PATH, detection_id='default_video'), content_type='multipart/x-mixed-replace; boundary=frame')

def live_feed(request):
    camera_index = request.GET.get('camera_index', '0')
    try:
        camera_index = int(camera_index)
    except ValueError:
        camera_index = 0
    return StreamingHttpResponse(stream_video(camera_index, detection_id=f'live_{camera_index}'), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'detection/index.html')

def live_camera(request):
    return render(request, 'detection/live_camera.html')

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media', 'videos'))
        filename = fs.save(video_file.name, video_file)
        video_path = fs.path(filename)
        
        # Guardar ruta en sesion o pasar a plantilla
        # Pasar nombre de archivo a plantilla
        return render(request, 'detection/upload_video.html', {
            'uploaded_video_url': filename
        })
    return render(request, 'detection/upload_video.html')

def uploaded_video_feed(request, filename):
    video_path = os.path.join(BASE_DIR, 'media', 'videos', filename)
    return StreamingHttpResponse(stream_video(video_path, detection_id=f'upload_{filename}'), content_type='multipart/x-mixed-replace; boundary=frame')

def get_latest_plate(request):
    detection_id = request.GET.get('detection_id')
    plate = latest_detections.get(detection_id, "")
    return JsonResponse({'plate': plate})
