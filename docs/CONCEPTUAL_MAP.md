# 🗺️ Mapa Conceptual: IA en MoveTracker

## Diagrama Principal - Ecosistema de IA

```mermaid
mindmap
  root((MoveTracker<br/>Sistema Inteligente))
    Computer Vision
      ALPR
        YOLO v8
        EasyOCR
        Detección Automática
        Registro de Entrada/Salida
      Detección de Ocupación
        CNN
        Monitoreo en Tiempo Real
        Mapas de Calor
      Clasificación de Vehículos
        Transfer Learning
        Identificación de Tipo
        Validación Automática
    Machine Learning
      Predicción de Demanda
        Random Forest
        LSTM
        Series Temporales
        Prophet
      Sistema de Recomendaciones
        Collaborative Filtering
        Espacios Óptimos
        Horarios Sugeridos
      Detección de Anomalías
        Isolation Forest
        Autoencoders
        Alertas de Fraude
    Procesamiento de Lenguaje Natural
      Chatbot Inteligente
        Rasa
        LangChain
        Atención 24/7
        Soporte en Español
      Análisis de Sentimientos
        VADER
        Hugging Face
        Feedback de Usuarios
    Optimización
      Asignación de Espacios
        Algoritmos Genéticos
        Reinforcement Learning
        Minimización de Distancia
      Pricing Dinámico
        Ajuste por Demanda
        Maximización de Ingresos
        Descuentos Inteligentes
    IoT y Edge Computing
      Sensores Inteligentes
        Raspberry Pi
        TensorFlow Lite
        Procesamiento Local
      Digital Twin
        Visualización 3D
        Simulación
        Planificación
```

---

## Diagrama de Relaciones - Tecnologías y Aplicaciones

```mermaid
graph TB
    subgraph "ENTRADA DE DATOS"
        A1[Cámaras IP<br/>RTSP Streams]
        A2[Sensores IoT<br/>MQTT]
        A3[Datos Históricos<br/>PostgreSQL]
        A4[Usuarios<br/>Interacciones]
    end

    subgraph "PROCESAMIENTO IA"
        B1[YOLO v8<br/>Detección]
        B2[EasyOCR<br/>Reconocimiento]
        B3[Random Forest<br/>Predicción]
        B4[Rasa/LangChain<br/>NLP]
        B5[Isolation Forest<br/>Anomalías]
    end

    subgraph "MODELOS DJANGO"
        C1[PlateDetection]
        C2[VehicleEntry]
        C3[DemandForecast]
        C4[ChatMessage]
        C5[AnomalyAlert]
    end

    subgraph "APLICACIONES"
        D1[Entrada/Salida<br/>Automática]
        D2[Predicción<br/>Ocupación]
        D3[Asistente<br/>Virtual]
        D4[Sistema de<br/>Alertas]
        D5[Pricing<br/>Dinámico]
    end

    subgraph "BENEFICIOS"
        E1[⚡ Eficiencia<br/>Operativa]
        E2[🔒 Mayor<br/>Seguridad]
        E3[😊 Mejor<br/>Experiencia]
        E4[💰 Incremento<br/>Ingresos]
    end

    A1 --> B1
    A1 --> B2
    A2 --> B5
    A3 --> B3
    A4 --> B4

    B1 --> C1
    B2 --> C1
    B3 --> C3
    B4 --> C4
    B5 --> C5

    C1 --> D1
    C2 --> D1
    C3 --> D2
    C3 --> D5
    C4 --> D3
    C5 --> D4

    D1 --> E1
    D1 --> E2
    D2 --> E1
    D2 --> E4
    D3 --> E3
    D4 --> E2
    D5 --> E4

    style B1 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style B2 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style B3 fill:#4ecdc4,stroke:#0a9396,color:#fff
    style B4 fill:#95e1d3,stroke:#38a3a5,color:#000
    style B5 fill:#ffd93d,stroke:#f9c74f,color:#000
    style E1 fill:#51cf66,stroke:#2f9e44,color:#fff
    style E2 fill:#51cf66,stroke:#2f9e44,color:#fff
    style E3 fill:#51cf66,stroke:#2f9e44,color:#fff
    style E4 fill:#51cf66,stroke:#2f9e44,color:#fff
```

---

## Flujo de Proceso ALPR (Reconocimiento de Placas)

```mermaid
flowchart TD
    START([Vehículo se acerca]) --> CAPTURE[Cámara captura frame]
    CAPTURE --> CELERY{Celery Task<br/>Asíncrono}
    
    CELERY --> DETECT[YOLO v8:<br/>Detectar ubicación de placa]
    DETECT --> CHECK_CONF{Confianza<br/>> 70%?}
    
    CHECK_CONF -->|No| LOG_FAIL[Registrar fallo]
    CHECK_CONF -->|Sí| CROP[Recortar región<br/>de la placa]
    
    CROP --> OCR[EasyOCR:<br/>Leer texto de placa]
    OCR --> VALIDATE{Formato<br/>válido?}
    
    VALIDATE -->|No| MANUAL[Marcado para<br/>revisión manual]
    VALIDATE -->|Sí| SAVE_DETECTION[Guardar en<br/>PlateDetection]
    
    SAVE_DETECTION --> SEARCH_DB{Vehículo<br/>registrado?}
    
    SEARCH_DB -->|No| ALERT[Alerta: Vehículo<br/>no autorizado]
    SEARCH_DB -->|Sí| CHECK_LOC{Ubicación<br/>cámara?}
    
    CHECK_LOC -->|Entrada| CREATE_ENTRY[Crear VehicleEntry<br/>entry_time = NOW]
    CHECK_LOC -->|Salida| UPDATE_EXIT[Actualizar VehicleEntry<br/>exit_time = NOW]
    
    CREATE_ENTRY --> ASSIGN_SPACE[Asignar espacio<br/>automáticamente]
    UPDATE_EXIT --> CALC_COST[Calcular costo<br/>según tarifa + tiempo]
    
    ASSIGN_SPACE --> NOTIFY_USER[Notificar usuario:<br/>Espacio asignado]
    CALC_COST --> GENERATE_BILL[Generar factura]
    
    NOTIFY_USER --> END([Proceso completado])
    GENERATE_BILL --> END
    ALERT --> END
    MANUAL --> END
    LOG_FAIL --> END

    style START fill:#74c0fc,stroke:#1864ab
    style END fill:#74c0fc,stroke:#1864ab
    style DETECT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style OCR fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style ALERT fill:#ffd93d,stroke:#f9c74f
    style GENERATE_BILL fill:#51cf66,stroke:#2f9e44,color:#fff
```

---

## Arquitectura de Capas - Sistema de IA

```mermaid
graph TB
    subgraph CAPA_1["🖥️ CAPA DE PRESENTACIÓN"]
        WEB[Web Client<br/>Django Templates]
        MOBILE[Mobile App<br/>React Native]
        DASHBOARD[Dashboard Analytics<br/>Grafana/Plotly]
    end

    subgraph CAPA_2["🔌 CAPA DE API"]
        REST[REST API<br/>Django REST Framework]
        WS[WebSockets<br/>Django Channels]
        GRAPHQL[GraphQL<br/>Graphene]
    end

    subgraph CAPA_3["🧠 CAPA DE IA/ML"]
        ALPR_SVC[ALPR Service<br/>YOLO + OCR]
        FORECAST_SVC[Demand Forecaster<br/>ML Models]
        CHAT_SVC[Chatbot Service<br/>NLP]
        ANOMALY_SVC[Anomaly Detector<br/>Unsupervised]
        OPTIMIZER[Space Optimizer<br/>Algorithms]
    end

    subgraph CAPA_4["⚙️ CAPA DE PROCESAMIENTO"]
        CELERY[Celery Workers<br/>Async Tasks]
        REDIS[Redis Cache<br/>+ Message Queue]
        KAFKA[Kafka Streams<br/>Event Processing]
    end

    subgraph CAPA_5["💾 CAPA DE DATOS"]
        POSTGRES[PostgreSQL<br/>Relational DB]
        TIMESCALE[TimescaleDB<br/>Time Series]
        MINIO[MinIO/S3<br/>Image Storage]
        ELASTIC[Elasticsearch<br/>Logs & Search]
    end

    subgraph CAPA_6["🎥 CAPA DE HARDWARE"]
        CAMERAS[IP Cameras<br/>RTSP Streams]
        SENSORS[IoT Sensors<br/>MQTT Protocol]
        GPU[GPU Server<br/>NVIDIA CUDA]
        EDGE[Edge Devices<br/>Raspberry Pi]
    end

    WEB --> REST
    MOBILE --> REST
    DASHBOARD --> GRAPHQL
    
    REST --> ALPR_SVC
    REST --> FORECAST_SVC
    WS --> CHAT_SVC
    GRAPHQL --> ANOMALY_SVC
    
    ALPR_SVC --> CELERY
    FORECAST_SVC --> CELERY
    CHAT_SVC --> REDIS
    ANOMALY_SVC --> KAFKA
    OPTIMIZER --> REDIS
    
    CELERY --> POSTGRES
    CELERY --> MINIO
    REDIS --> TIMESCALE
    KAFKA --> ELASTIC
    
    CAMERAS --> ALPR_SVC
    SENSORS --> ANOMALY_SVC
    GPU --> ALPR_SVC
    EDGE --> SENSORS

    classDef layer1 fill:#e7f5ff,stroke:#1864ab
    classDef layer2 fill:#d0ebff,stroke:#1971c2
    classDef layer3 fill:#ffc9c9,stroke:#c92a2a
    classDef layer4 fill:#d3f9d8,stroke:#2f9e44
    classDef layer5 fill:#fff3bf,stroke:#f08c00
    classDef layer6 fill:#e3fafc,stroke:#0b7285

    class WEB,MOBILE,DASHBOARD layer1
    class REST,WS,GRAPHQL layer2
    class ALPR_SVC,FORECAST_SVC,CHAT_SVC,ANOMALY_SVC,OPTIMIZER layer3
    class CELERY,REDIS,KAFKA layer4
    class POSTGRES,TIMESCALE,MINIO,ELASTIC layer5
    class CAMERAS,SENSORS,GPU,EDGE layer6
```

---

## Timeline de Implementación

```mermaid
gantt
    title Roadmap de Implementación IA - MoveTracker
    dateFormat YYYY-MM-DD
    section Fase 1: Fundamentos
    Setup Infraestructura         :2026-01-01, 30d
    Configurar Docker + GPU        :2026-01-15, 20d
    Instalar Dependencias IA       :2026-02-01, 15d
    
    section Fase 2: ALPR
    Implementar YOLO v8            :2026-02-15, 25d
    Integrar EasyOCR               :2026-03-01, 20d
    Pruebas en Campo               :2026-03-15, 20d
    Fine-tuning Modelos            :2026-03-25, 15d
    
    section Fase 3: Predicción
    Recolección Datos Históricos   :2026-04-01, 30d
    Entrenar Modelo Forecasting    :2026-05-01, 25d
    API de Predicciones            :2026-05-20, 15d
    
    section Fase 4: Optimización
    Algoritmo Asignación Espacios  :2026-06-01, 20d
    Sistema Recomendaciones        :2026-06-15, 20d
    Pricing Dinámico               :2026-07-01, 15d
    
    section Fase 5: NLP
    Implementar Chatbot            :2026-07-15, 30d
    Integrar WhatsApp/Telegram     :2026-08-10, 20d
    Análisis de Sentimientos       :2026-08-25, 15d
    
    section Fase 6: Avanzado
    Detección de Anomalías         :2026-09-01, 25d
    Edge Computing (Raspberry Pi)  :2026-10-01, 30d
    Digital Twin 3D                :2026-11-01, 30d
    Optimización Final             :2026-12-01, 30d
```

---

## Matriz de Prioridades - Impacto vs Esfuerzo

```mermaid
quadrantChart
    title Priorización de Funcionalidades IA
    x-axis Bajo Esfuerzo --> Alto Esfuerzo
    y-axis Bajo Impacto --> Alto Impacto
    quadrant-1 Planificar
    quadrant-2 Implementar YA
    quadrant-3 Evitar/Posponer
    quadrant-4 Evaluar
    
    ALPR Básico: [0.35, 0.85]
    Predicción Demanda: [0.50, 0.75]
    Chatbot: [0.45, 0.60]
    Pricing Dinámico: [0.55, 0.70]
    Digital Twin: [0.85, 0.60]
    Detección Anomalías: [0.40, 0.55]
    Edge Computing: [0.75, 0.50]
    Análisis Sentimientos: [0.30, 0.35]
    Optimización Espacios: [0.60, 0.80]
    Clasificación Vehículos: [0.40, 0.45]
```

---

## Diagrama de Flujo de Datos - Sistema Completo

```mermaid
flowchart LR
    subgraph INPUT["📥 ENTRADA"]
        CAM[Cámaras]
        SENS[Sensores]
        USERS[Usuarios]
        HIST[Históricos]
    end

    subgraph PROCESSING["⚙️ PROCESAMIENTO"]
        QUEUE[Cola de Tareas<br/>Celery + Redis]
        
        subgraph AI["🧠 MÓDULOS IA"]
            VISION[Computer Vision]
            ML[Machine Learning]
            NLP[NLP]
            OPT[Optimización]
        end
    end

    subgraph STORAGE["💾 ALMACENAMIENTO"]
        DB[(PostgreSQL)]
        TS[(TimescaleDB)]
        OBJ[Object Storage]
        CACHE[(Redis Cache)]
    end

    subgraph OUTPUT["📤 SALIDA"]
        API[REST API]
        NOTIF[Notificaciones]
        DASH[Dashboards]
        REPORTS[Reportes]
    end

    CAM --> QUEUE
    SENS --> QUEUE
    USERS --> QUEUE
    HIST --> ML

    QUEUE --> VISION
    QUEUE --> ML
    QUEUE --> NLP
    QUEUE --> OPT

    VISION --> DB
    VISION --> OBJ
    ML --> TS
    ML --> CACHE
    NLP --> DB
    OPT --> CACHE

    DB --> API
    TS --> DASH
    CACHE --> API
    OBJ --> API

    API --> NOTIF
    API --> DASH
    DASH --> REPORTS

    style VISION fill:#ff6b6b,color:#fff
    style ML fill:#4ecdc4,color:#fff
    style NLP fill:#95e1d3
    style OPT fill:#ffd93d
```

---

## Modelo de Datos Extendido con IA

```mermaid
erDiagram
    USER ||--o{ VEHICLE : owns
    USER ||--o{ CHAT_MESSAGE : sends
    USER ||--o{ PARKING_CONFIG : creates
    
    VEHICLE ||--o{ VEHICLE_ENTRY : has
    VEHICLE ||--o{ PLATE_DETECTION : detected_as
    VEHICLE }o--|| VEHICLE_TYPE : is_of_type
    
    CAMERA_STATION ||--o{ PLATE_DETECTION : captures
    PARKING_FLOOR ||--|| CAMERA_STATION : monitors
    
    VEHICLE_ENTRY }o--|| PARKING_SPACE : occupies
    VEHICLE_ENTRY }o--|| PLATE_DETECTION : triggered_by
    
    PARKING_SPACE }o--|| PARKING_FLOOR : located_in
    PARKING_SPACE ||--o{ OCCUPANCY_SNAPSHOT : tracked_in
    
    PARKING_CONFIG ||--o{ PARKING_FLOOR : defines
    
    DEMAND_FORECAST ||--|| PARKING_FLOOR : predicts_for
    ANOMALY_ALERT ||--|| PARKING_SPACE : detected_in
    
    USER {
        int id PK
        string username
        string email
        string role
    }
    
    VEHICLE {
        int id PK
        int owner_id FK
        string license_plate UK
        string vehicle_type
        string brand
        string model
        string color
    }
    
    CAMERA_STATION {
        int id PK
        string name
        string location
        string ip_address
        string rtsp_url
        string ai_model_version
        boolean is_active
    }
    
    PLATE_DETECTION {
        int id PK
        int camera_id FK
        string license_plate
        datetime detection_time
        float confidence_score
        string image_path
        int bbox_x
        int bbox_y
        int bbox_width
        int bbox_height
        boolean is_verified
    }
    
    VEHICLE_ENTRY {
        int id PK
        int vehicle_id FK
        int plate_detection_id FK
        datetime entry_time
        datetime exit_time
        int assigned_space_id FK
        string detection_method
        decimal total_cost
    }
    
    PARKING_SPACE {
        int id PK
        int floor_id FK
        string space_number
        boolean is_occupied
        string ai_occupancy_status
        datetime last_ai_check
        float confidence_score
    }
    
    DEMAND_FORECAST {
        int id PK
        date forecast_date
        int hour
        int predicted_occupancy
        int confidence_interval_low
        int confidence_interval_high
        int actual_occupancy
        string model_version
    }
    
    CHAT_MESSAGE {
        int id PK
        int user_id FK
        text message
        text response
        string intent_detected
        float confidence
        datetime timestamp
    }
    
    ANOMALY_ALERT {
        int id PK
        int space_id FK
        string anomaly_type
        text description
        datetime detected_at
        string severity
        boolean is_resolved
    }
```

---

## Stack Tecnológico Completo

```mermaid
graph TD
    subgraph FRONTEND["💻 FRONTEND"]
        F1[Django Templates]
        F2[React/React Native]
        F3[Plotly Dash]
    end

    subgraph BACKEND["🔧 BACKEND"]
        B1[Django 4.2]
        B2[Django REST Framework]
        B3[Django Channels]
        B4[Celery]
    end

    subgraph AI_ML["🤖 IA/ML"]
        A1[PyTorch 2.1]
        A2[TensorFlow 2.15]
        A3[YOLO v8]
        A4[EasyOCR]
        A5[Scikit-learn]
        A6[XGBoost]
        A7[Rasa / LangChain]
        A8[OpenCV]
    end

    subgraph DATA["📊 DATOS"]
        D1[PostgreSQL 15]
        D2[TimescaleDB]
        D3[Redis 7]
        D4[MinIO/S3]
        D5[Elasticsearch]
    end

    subgraph INFRA["🏗️ INFRAESTRUCTURA"]
        I1[Docker]
        I2[Kubernetes]
        I3[NGINX]
        I4[Gunicorn]
    end

    subgraph HARDWARE["🎥 HARDWARE"]
        H1[IP Cameras]
        H2[NVIDIA GPU]
        H3[Raspberry Pi 4]
        H4[IoT Sensors]
    end

    F1 --> B1
    F2 --> B2
    F3 --> B2

    B1 --> B4
    B2 --> B4
    B3 --> B4

    B4 --> A1
    B4 --> A3
    B4 --> A4
    B4 --> A5
    B4 --> A7
    B4 --> A8

    A1 --> D1
    A3 --> D4
    A5 --> D2
    A7 --> D3

    D1 --> I1
    D2 --> I1
    D3 --> I1

    I1 --> I2
    I2 --> I3
    I3 --> I4

    H1 --> A3
    H2 --> A1
    H3 --> A8
    H4 --> D3

    style AI_ML fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style DATA fill:#4ecdc4,stroke:#0a9396,color:#fff
    style HARDWARE fill:#ffd93d,stroke:#f9c74f
```

---

## Conclusión Visual

```mermaid
mindmap
  root((MoveTracker<br/>IA Integrada))
    Beneficios Cuantificables
      95% Precisión ALPR
      40% Menos tiempo búsqueda
      20% Incremento ingresos
      99.5% Uptime sistema
    Ventajas Competitivas
      Automatización completa
      Experiencia superior
      Seguridad mejorada
      Escalabilidad probada
    Tecnología de Punta
      Deep Learning
      Edge Computing
      Real-time Processing
      Predictive Analytics
    ROI Estimado
      Recuperación 18 meses
      Reducción costos 30%
      Mayor satisfacción
      Diferenciación mercado
```

---

**Documento generado:** 25 de Octubre, 2025  
**Versión:** 1.0  
**Herramienta:** Mermaid.js para diagramas interactivos
