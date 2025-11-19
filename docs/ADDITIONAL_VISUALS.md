# 🎨 Visualizaciones Adicionales: IA en MoveTracker

**Proyecto:** MoveTracker Smart Parking System  
**Propósito:** Representaciones visuales alternativas de la investigación de IA  
**Fecha:** 25 de Octubre, 2025

---

## 📊 Gráfico de Radar: Capacidades del Sistema

```mermaid
---
config:
  themeVariables:
    quadrant1Fill: '#ff6b6b'
    quadrant2Fill: '#4ecdc4'
    quadrant3Fill: '#95e1d3'
    quadrant4Fill: '#ffd93d'
---
pie title Distribución de Tecnologías IA
    "Computer Vision (ALPR)" : 30
    "Machine Learning Predictivo" : 25
    "NLP y Chatbots" : 15
    "Optimización Algorítmica" : 15
    "IoT y Edge Computing" : 10
    "Analytics y BI" : 5
```

---

## 🔄 Flujo de Integración de Datos

```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web/Mobile
    participant API as Django API
    participant C as Celery Worker
    participant AI as Módulos IA
    participant DB as PostgreSQL
    participant Cache as Redis
    
    U->>W: Solicita reservación
    W->>API: POST /api/reservations/
    API->>DB: Verificar disponibilidad
    DB-->>API: Espacios disponibles
    
    API->>C: Tarea async: optimizar_espacio
    C->>AI: Ejecutar algoritmo
    AI->>Cache: Obtener predicciones
    Cache-->>AI: Demanda próximas 24h
    AI->>AI: Calcular espacio óptimo
    AI-->>C: Resultado: Espacio #42, Piso 2
    
    C->>DB: Guardar asignación
    C-->>API: Task completada
    API-->>W: Confirmación + QR code
    W-->>U: Notificación push
    
    Note over U,Cache: Proceso completo: ~3 segundos
```

---

## 🏛️ Arquitectura Detallada por Capas

```mermaid
graph TD
    subgraph USERS["👥 USUARIOS"]
        U1[Clientes Web]
        U2[Clientes Mobile]
        U3[Administradores]
        U4[Trabajadores]
    end

    subgraph PRESENTATION["🖥️ PRESENTACIÓN"]
        P1[Django Templates]
        P2[React Native App]
        P3[Admin Dashboard]
        P4[Grafana Analytics]
    end

    subgraph APPLICATION["⚙️ APLICACIÓN"]
        A1[Django Views]
        A2[DRF ViewSets]
        A3[Django Channels]
        A4[Business Logic]
    end

    subgraph AI_SERVICES["🤖 SERVICIOS IA"]
        direction TB
        AI1[ALPR Service<br/>📸 Computer Vision]
        AI2[Demand Forecaster<br/>📈 ML Predictivo]
        AI3[Space Optimizer<br/>🎯 Algoritmos]
        AI4[Chatbot Service<br/>💬 NLP]
        AI5[Anomaly Detector<br/>🚨 Seguridad]
        AI6[Price Optimizer<br/>💰 Pricing]
    end

    subgraph PROCESSING["🔧 PROCESAMIENTO"]
        PR1[Celery Workers]
        PR2[Redis Queue]
        PR3[Message Broker]
        PR4[Background Jobs]
    end

    subgraph DATA_LAYER["💾 DATOS"]
        D1[(PostgreSQL<br/>Datos estructurados)]
        D2[(TimescaleDB<br/>Series temporales)]
        D3[(Redis<br/>Cache + Queue)]
        D4[(MinIO<br/>Imágenes/Videos)]
        D5[(Elasticsearch<br/>Logs + Search)]
    end

    subgraph INFRASTRUCTURE["🏗️ INFRAESTRUCTURA"]
        I1[Docker Containers]
        I2[NGINX Load Balancer]
        I3[Kubernetes Cluster]
        I4[Monitoring Stack]
    end

    subgraph HARDWARE_LAYER["🎥 HARDWARE"]
        H1[IP Cameras x4]
        H2[GPU Server NVIDIA]
        H3[Raspberry Pi Edge]
        H4[IoT Sensors]
    end

    U1 --> P1
    U2 --> P2
    U3 --> P3
    U4 --> P4

    P1 --> A1
    P2 --> A2
    P3 --> A2
    P4 --> A3

    A1 --> AI1
    A2 --> AI2
    A2 --> AI3
    A3 --> AI4
    A4 --> AI5
    A4 --> AI6

    AI1 --> PR1
    AI2 --> PR1
    AI3 --> PR2
    AI4 --> PR2
    AI5 --> PR3
    AI6 --> PR2

    PR1 --> D1
    PR1 --> D4
    PR2 --> D3
    PR3 --> D5
    PR4 --> D2

    D1 --> I1
    D2 --> I1
    D3 --> I1
    D4 --> I1
    D5 --> I1

    I1 --> I2
    I2 --> I3
    I3 --> I4

    H1 --> AI1
    H2 --> AI1
    H2 --> AI2
    H3 --> AI1
    H4 --> AI5

    classDef userClass fill:#e7f5ff,stroke:#1864ab,stroke-width:2px
    classDef presentClass fill:#d0ebff,stroke:#1971c2,stroke-width:2px
    classDef appClass fill:#a5d8ff,stroke:#1c7ed6,stroke-width:2px
    classDef aiClass fill:#ffc9c9,stroke:#c92a2a,stroke-width:3px
    classDef procClass fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px
    classDef dataClass fill:#fff3bf,stroke:#f08c00,stroke-width:2px
    classDef infraClass fill:#e3fafc,stroke:#0b7285,stroke-width:2px
    classDef hardClass fill:#f3d9fa,stroke:#9c36b5,stroke-width:2px

    class U1,U2,U3,U4 userClass
    class P1,P2,P3,P4 presentClass
    class A1,A2,A3,A4 appClass
    class AI1,AI2,AI3,AI4,AI5,AI6 aiClass
    class PR1,PR2,PR3,PR4 procClass
    class D1,D2,D3,D4,D5 dataClass
    class I1,I2,I3,I4 infraClass
    class H1,H2,H3,H4 hardClass
```

---

## 🔀 Diagrama de Estados: Ciclo de Vida del Vehículo

```mermaid
stateDiagram-v2
    [*] --> NoRegistrado: Vehículo se acerca
    
    NoRegistrado --> DeteccionPlaca: Cámara captura
    DeteccionPlaca --> Procesamiento: YOLO + OCR
    
    Procesamiento --> Reconocido: Placa en BD
    Procesamiento --> NoReconocido: Placa no encontrada
    
    NoReconocido --> AlertaSeguridad: Sin autorización
    NoReconocido --> RegistroManual: Operador interviene
    
    RegistroManual --> Reconocido: Registro completado
    
    Reconocido --> BusquedaEspacio: Sistema asigna
    BusquedaEspacio --> EspacioAsignado: Algoritmo optimización
    
    EspacioAsignado --> Estacionado: Vehículo entra
    Estacionado --> EnEspera: Usuario ausente
    
    EnEspera --> Salida: Usuario retorna
    Salida --> CalculoCosto: Detección salida
    
    CalculoCosto --> PagoGenerado: Factura creada
    PagoGenerado --> PagoPendiente: Esperando pago
    
    PagoPendiente --> PagoCompletado: Pago confirmado
    PagoPendiente --> Moroso: Timeout
    
    Moroso --> PagoCompletado: Pago recibido
    
    PagoCompletado --> Liberado: Barrera abierta
    Liberado --> [*]: Vehículo sale
    
    AlertaSeguridad --> [*]: Acceso denegado
    
    note right of Procesamiento
        ALPR con IA:
        - YOLO v8
        - EasyOCR
        - Confianza > 70%
    end note
    
    note right of BusquedaEspacio
        Optimización con ML:
        - Historial usuario
        - Predicción demanda
        - Minimizar distancia
    end note
```

---

## 📈 Dashboard Conceptual: Métricas en Tiempo Real

```mermaid
graph TB
    subgraph DASHBOARD["📊 DASHBOARD PRINCIPAL"]
        direction TB
        
        subgraph METRICS["Métricas Clave"]
            M1[⚡ Ocupación Actual<br/>85/100 espacios<br/>85%]
            M2[💰 Ingresos Hoy<br/>$4,250<br/>+12% vs ayer]
            M3[🚗 Vehículos Hoy<br/>142 entradas<br/>38 activos]
            M4[⏱️ Tiempo Promedio<br/>2.5 horas<br/>-15% vs semana]
        end
        
        subgraph AI_INSIGHTS["🧠 Insights de IA"]
            I1[📈 Predicción 4pm<br/>Ocupación: 95%<br/>⚠️ Pico esperado]
            I2[🎯 Espacios Óptimos<br/>Piso 2: 15 libres<br/>✅ Recomendado]
            I3[🚨 Anomalías<br/>2 detectadas<br/>⚠️ Revisar]
            I4[💬 Chatbot<br/>45 consultas<br/>92% resueltas]
        end
        
        subgraph REALTIME["📡 Tiempo Real"]
            R1[🎥 ALPR Status<br/>4/4 cámaras OK<br/>✅ Funcionando]
            R2[🔄 Cola Celery<br/>12 tareas<br/>⏳ Procesando]
            R3[💾 Base de Datos<br/>2.3ms latencia<br/>✅ Óptimo]
            R4[🌐 API Status<br/>99.8% uptime<br/>✅ Saludable]
        end
        
        subgraph CHARTS["📊 Gráficos"]
            C1[Ocupación Hoy<br/>Línea temporal]
            C2[Ingresos Semana<br/>Barras]
            C3[Tipos Vehículo<br/>Pastel]
            C4[Heatmap Pisos<br/>Mapa calor]
        end
    end
    
    M1 -.-> I1
    M3 -.-> R1
    I1 -.-> C1
    M2 -.-> C2
    M3 -.-> C3
    I2 -.-> C4

    style M1 fill:#51cf66,color:#000
    style M2 fill:#ffd93d,color:#000
    style M3 fill:#74c0fc,color:#000
    style M4 fill:#b197fc,color:#000
    style I1 fill:#ffa94d,color:#000
    style I2 fill:#51cf66,color:#000
    style I3 fill:#ff6b6b,color:#fff
    style I4 fill:#4ecdc4,color:#000
```

---

## 🗂️ Taxonomía de Modelos de IA

```mermaid
mindmap
  root((Modelos IA<br/>MoveTracker))
    Supervisados
      Clasificación
        SVM: Tipo Vehículo
        Random Forest: Fraude
        Redes Neuronales: Intents
      Regresión
        Linear: Precio base
        Ridge: Demanda simple
        LSTM: Series temporales
      Secuencia
        RNN: Texto chatbot
        Transformer: NLP avanzado
    No Supervisados
      Clustering
        K-Means: Segmentación usuarios
        DBSCAN: Patrones uso
      Reducción Dimensionalidad
        PCA: Features
        Autoencoders: Compresión
      Detección Anomalías
        Isolation Forest: Fraudes
        One-Class SVM: Outliers
    Reinforcement Learning
      Q-Learning
        Asignación espacios
      Policy Gradient
        Pricing dinámico
      Deep Q-Network
        Optimización global
    Computer Vision
      Object Detection
        YOLO v8: Placas
        Faster R-CNN: Vehículos
      Segmentación
        Mask R-CNN: Espacios
      Clasificación
        ResNet: Tipo vehículo
        MobileNet: Edge devices
    NLP
      Intent Recognition
        BERT: Chatbot
        DistilBERT: Lightweight
      Sentiment Analysis
        VADER: Español
        RoBERTa: Fine-tuned
      Generation
        GPT-3.5: Respuestas
        LangChain: Orchestration
```

---

## 🔐 Diagrama de Seguridad y Privacidad

```mermaid
graph TD
    subgraph EXTERNAL["🌐 MUNDO EXTERNO"]
        USER[Usuario]
        ATTACKER[Posible Atacante]
    end
    
    subgraph SECURITY_LAYERS["🛡️ CAPAS DE SEGURIDAD"]
        
        subgraph LAYER1["Capa 1: Perímetro"]
            FW[Firewall<br/>Cloudflare]
            WAF[Web Application<br/>Firewall]
            DDOS[Protección<br/>DDoS]
        end
        
        subgraph LAYER2["Capa 2: Aplicación"]
            NGINX[NGINX<br/>Rate Limiting]
            SSL[SSL/TLS<br/>Let's Encrypt]
            AUTH[Autenticación<br/>JWT + OAuth2]
        end
        
        subgraph LAYER3["Capa 3: Lógica"]
            RBAC[Control Acceso<br/>Basado en Roles]
            INPUT_VAL[Validación<br/>de Entrada]
            CSRF[Protección<br/>CSRF/XSS]
        end
        
        subgraph LAYER4["Capa 4: Datos"]
            ENCRYPT[Encriptación<br/>AES-256]
            ANON[Anonimización<br/>Datos Sensibles]
            BACKUP[Backups<br/>Encriptados]
        end
        
        subgraph LAYER5["Capa 5: Infraestructura"]
            CONTAINER[Aislamiento<br/>Containers]
            SECRETS[Gestión<br/>Secrets (Vault)]
            AUDIT[Logs de<br/>Auditoría]
        end
    end
    
    subgraph PRIVACY["🔒 PRIVACIDAD"]
        GDPR[Cumplimiento<br/>GDPR]
        CONSENT[Consentimiento<br/>Explícito]
        RETENTION[Política<br/>Retención 30d]
        RIGHT_DELETE[Derecho al<br/>Olvido]
    end
    
    subgraph AI_SECURITY["🤖 SEGURIDAD IA"]
        MODEL_SEC[Modelos<br/>Firmados]
        ADVERSARIAL[Protección<br/>Adversarial]
        EXPLAINABILITY[Explicabilidad<br/>Decisiones IA]
    end
    
    USER --> FW
    ATTACKER -.Bloqueo.-> FW
    
    FW --> WAF
    WAF --> DDOS
    DDOS --> NGINX
    
    NGINX --> SSL
    SSL --> AUTH
    AUTH --> RBAC
    
    RBAC --> INPUT_VAL
    INPUT_VAL --> CSRF
    CSRF --> ENCRYPT
    
    ENCRYPT --> ANON
    ANON --> BACKUP
    BACKUP --> CONTAINER
    
    CONTAINER --> SECRETS
    SECRETS --> AUDIT
    
    AUDIT --> GDPR
    GDPR --> CONSENT
    CONSENT --> RETENTION
    RETENTION --> RIGHT_DELETE
    
    ENCRYPT --> MODEL_SEC
    MODEL_SEC --> ADVERSARIAL
    ADVERSARIAL --> EXPLAINABILITY

    style FW fill:#ff6b6b,color:#fff
    style WAF fill:#ff6b6b,color:#fff
    style DDOS fill:#ff6b6b,color:#fff
    style ENCRYPT fill:#51cf66,color:#000
    style ANON fill:#51cf66,color:#000
    style GDPR fill:#4ecdc4,color:#000
    style MODEL_SEC fill:#ffa94d,color:#000
```

---

## 📊 Comparativa: Antes vs Después de IA

```mermaid
graph LR
    subgraph BEFORE["❌ SISTEMA TRADICIONAL"]
        B1[Entrada Manual<br/>⏱️ 2-3 min/vehículo]
        B2[Asignación Aleatoria<br/>🎲 Sin optimización]
        B3[Tarifas Fijas<br/>💵 $5/hora siempre]
        B4[Búsqueda Manual<br/>🚶 5-10 min promedio]
        B5[Sin Predicción<br/>❓ Planificación nula]
        B6[Atención Limitada<br/>🕐 8am - 6pm]
        B7[Errores Humanos<br/>📝 10% tasa error]
        B8[Reporte Semanal<br/>📅 Datos obsoletos]
    end
    
    subgraph AFTER["✅ SISTEMA CON IA"]
        A1[ALPR Automático<br/>⚡ 2 segundos]
        A2[Asignación Inteligente<br/>🎯 Optimizada]
        A3[Pricing Dinámico<br/>💰 +20% ingresos]
        A4[Navegación Guiada<br/>📍 1-2 min promedio]
        A5[Forecasting ML<br/>📈 95% precisión]
        A6[Chatbot 24/7<br/>🤖 Siempre disponible]
        A7[Precisión IA<br/>✅ 95% accuracy]
        A8[Analytics Real-time<br/>⚡ Datos al instante]
    end
    
    B1 -.Reemplazado por.-> A1
    B2 -.Mejorado a.-> A2
    B3 -.Evolucionado a.-> A3
    B4 -.Optimizado a.-> A4
    B5 -.Transformado en.-> A5
    B6 -.Ampliado a.-> A6
    B7 -.Corregido con.-> A7
    B8 -.Actualizado a.-> A8

    style B1 fill:#ffc9c9,stroke:#c92a2a
    style B2 fill:#ffc9c9,stroke:#c92a2a
    style B3 fill:#ffc9c9,stroke:#c92a2a
    style B4 fill:#ffc9c9,stroke:#c92a2a
    style B5 fill:#ffc9c9,stroke:#c92a2a
    style B6 fill:#ffc9c9,stroke:#c92a2a
    style B7 fill:#ffc9c9,stroke:#c92a2a
    style B8 fill:#ffc9c9,stroke:#c92a2a
    
    style A1 fill:#d3f9d8,stroke:#2f9e44
    style A2 fill:#d3f9d8,stroke:#2f9e44
    style A3 fill:#d3f9d8,stroke:#2f9e44
    style A4 fill:#d3f9d8,stroke:#2f9e44
    style A5 fill:#d3f9d8,stroke:#2f9e44
    style A6 fill:#d3f9d8,stroke:#2f9e44
    style A7 fill:#d3f9d8,stroke:#2f9e44
    style A8 fill:#d3f9d8,stroke:#2f9e44
```

---

## 🎯 User Journey Map con IA

```mermaid
journey
    title Experiencia del Usuario con IA Integrada
    section Antes de Llegar
      Consulta disponibilidad en app: 5: Usuario
      IA predice ocupación futura: 5: Sistema
      Recibe recomendación de horario: 5: Usuario
      Hace reservación anticipada: 5: Usuario
    section Llegada
      Vehículo detectado por cámara: 5: Sistema
      ALPR reconoce placa automáticamente: 5: IA
      Recibe notificación push: 5: Usuario
      Espacio asignado inteligentemente: 5: IA
      Navega con mapa indoor: 5: Usuario
    section Estacionado
      Confirma llegada vía app: 5: Usuario
      Chatbot responde dudas: 5: IA
      Predicción de tiempo estimado: 4: IA
      Recibe descuentos personalizados: 5: Usuario
    section Salida
      Solicita vehículo por voz: 5: Usuario
      Costo calculado automáticamente: 5: Sistema
      Paga sin contacto (QR/NFC): 5: Usuario
      Barrera se abre automáticamente: 5: IA
      Encuesta de satisfacción: 4: Usuario
    section Post-Visita
      Recibe factura electrónica: 5: Sistema
      Análisis de sentimientos positivo: 5: IA
      Oferta personalizada siguiente visita: 5: Usuario
```

---

## 🔬 Proceso de Entrenamiento de Modelos

```mermaid
flowchart TD
    START([Inicio Entrenamiento]) --> COLLECT[📦 Recolección de Datos]
    
    COLLECT --> LABEL{Datos<br/>etiquetados?}
    LABEL -->|No| ANNOTATE[🏷️ Anotación Manual<br/>LabelImg/CVAT]
    ANNOTATE --> SPLIT
    LABEL -->|Sí| SPLIT[✂️ Split Dataset<br/>70% train / 15% val / 15% test]
    
    SPLIT --> PREPROCESS[⚙️ Preprocesamiento]
    PREPROCESS --> AUG[🔄 Data Augmentation<br/>Rotación, Flip, Zoom]
    
    AUG --> CHOOSE{Tipo de<br/>modelo?}
    
    CHOOSE -->|ALPR| YOLO[🎯 YOLO v8<br/>Object Detection]
    CHOOSE -->|Predicción| RF[🌲 Random Forest<br/>/ LSTM]
    CHOOSE -->|Chatbot| RASA[💬 Rasa NLU]
    
    YOLO --> TRAIN1[🏋️ Entrenamiento<br/>100 epochs]
    RF --> TRAIN2[🏋️ Entrenamiento<br/>Cross-validation]
    RASA --> TRAIN3[🏋️ Entrenamiento<br/>Intents + Stories]
    
    TRAIN1 --> EVAL1[📊 Evaluación<br/>mAP, Precision, Recall]
    TRAIN2 --> EVAL2[📊 Evaluación<br/>MAE, RMSE, R²]
    TRAIN3 --> EVAL3[📊 Evaluación<br/>Intent Accuracy]
    
    EVAL1 --> METRICS{Métricas<br/>aceptables?}
    EVAL2 --> METRICS
    EVAL3 --> METRICS
    
    METRICS -->|No| TUNE[🔧 Hyperparameter Tuning<br/>Grid/Random Search]
    TUNE --> CHOOSE
    
    METRICS -->|Sí| VALIDATE[✅ Validación Final<br/>Test Set]
    VALIDATE --> EXPORT[📤 Exportar Modelo<br/>.pt / .pkl / .tar.gz]
    
    EXPORT --> VERSION[🏷️ Versionado<br/>MLflow/DVC]
    VERSION --> DEPLOY[🚀 Deployment<br/>Docker + Kubernetes]
    
    DEPLOY --> MONITOR[📈 Monitoreo<br/>Prometheus + Grafana]
    MONITOR --> FEEDBACK{Performance<br/>degradado?}
    
    FEEDBACK -->|Sí| RETRAIN[🔄 Re-entrenamiento<br/>Con datos nuevos]
    RETRAIN --> COLLECT
    
    FEEDBACK -->|No| END([Modelo en Producción ✅])

    style START fill:#74c0fc,stroke:#1864ab
    style END fill:#51cf66,stroke:#2f9e44
    style YOLO fill:#ff6b6b,color:#fff
    style RF fill:#4ecdc4
    style RASA fill:#95e1d3
    style DEPLOY fill:#ffd93d
```

---

## 📱 Arquitectura Mobile con IA

```mermaid
graph TB
    subgraph MOBILE_APP["📱 APLICACIÓN MÓVIL"]
        UI[React Native UI]
        
        subgraph FEATURES["Funcionalidades"]
            F1[🔍 Buscar Espacios]
            F2[📅 Hacer Reserva]
            F3[🗺️ Navegación Indoor]
            F4[💳 Pago Digital]
            F5[💬 Chat con Bot]
            F6[📊 Historial]
        end
        
        subgraph LOCAL_AI["🤖 IA Local"]
            L1[TensorFlow Lite<br/>Clasificación rápida]
            L2[CoreML iOS<br/>Optimizado]
            L3[Offline Mode<br/>Cache inteligente]
        end
    end
    
    subgraph BACKEND["☁️ BACKEND"]
        API[REST API Django]
        
        subgraph SERVICES["Servicios IA"]
            S1[ALPR Service]
            S2[Recommender]
            S3[Chatbot Engine]
            S4[Analytics]
        end
        
        REALTIME[WebSocket<br/>Tiempo Real]
    end
    
    subgraph PUSH["📲 NOTIFICACIONES"]
        FCM[Firebase Cloud<br/>Messaging]
        APNS[Apple Push<br/>Notification]
    end
    
    UI --> F1
    UI --> F2
    UI --> F3
    UI --> F4
    UI --> F5
    UI --> F6
    
    F1 --> L1
    F3 --> L2
    F5 --> L3
    
    F1 --> API
    F2 --> API
    F4 --> API
    F5 --> API
    
    API --> S1
    API --> S2
    API --> S3
    API --> S4
    
    S2 --> REALTIME
    S3 --> REALTIME
    REALTIME --> UI
    
    S1 --> FCM
    S2 --> APNS
    FCM --> UI
    APNS --> UI

    style MOBILE_APP fill:#e7f5ff,stroke:#1864ab
    style L1 fill:#ff6b6b,color:#fff
    style L2 fill:#ff6b6b,color:#fff
    style S1 fill:#4ecdc4
    style S2 fill:#4ecdc4
    style S3 fill:#95e1d3
```

---

## 🌍 Mapa de Calor: Zonas de Ocupación

```mermaid
graph TD
    subgraph PARKING["🏢 ESTACIONAMIENTO - Vista Superior"]
        subgraph FLOOR3["Piso 3 - 🟢 Baja Ocupación 35%"]
            F3_Z1[Zona A<br/>2/10 ocupados]
            F3_Z2[Zona B<br/>3/10 ocupados]
            F3_Z3[Zona C<br/>2/10 ocupados]
        end
        
        subgraph FLOOR2["Piso 2 - 🟡 Media Ocupación 65%"]
            F2_Z1[Zona A<br/>7/10 ocupados]
            F2_Z2[Zona B<br/>6/10 ocupados]
            F2_Z3[Zona C<br/>6/10 ocupados]
        end
        
        subgraph FLOOR1["Piso 1 - 🔴 Alta Ocupación 92%"]
            F1_Z1[Zona A<br/>10/10 ocupados]
            F1_Z2[Zona B<br/>9/10 ocupados]
            F1_Z3[Zona C<br/>9/10 ocupados]
        end
        
        subgraph AI_REC["🤖 Recomendación IA"]
            REC[Sugerencia: Piso 3, Zona A<br/>✅ Cerca de elevador<br/>✅ Baja ocupación<br/>✅ Precio normal]
        end
    end
    
    F1_Z1 -.Alto tráfico.-> REC
    F3_Z1 -.Recomendado.-> REC

    style F3_Z1 fill:#d3f9d8,stroke:#2f9e44
    style F3_Z2 fill:#d3f9d8,stroke:#2f9e44
    style F3_Z3 fill:#d3f9d8,stroke:#2f9e44
    
    style F2_Z1 fill:#fff3bf,stroke:#f08c00
    style F2_Z2 fill:#fff3bf,stroke:#f08c00
    style F2_Z3 fill:#fff3bf,stroke:#f08c00
    
    style F1_Z1 fill:#ffc9c9,stroke:#c92a2a
    style F1_Z2 fill:#ffc9c9,stroke:#c92a2a
    style F1_Z3 fill:#ffc9c9,stroke:#c92a2a
    
    style REC fill:#4ecdc4,stroke:#0a9396,stroke-width:3px
```

---

## 📊 Métricas de Performance de Modelos

```mermaid
graph LR
    subgraph ALPR_METRICS["🎯 ALPR Performance"]
        A1[Precisión: 96.2%]
        A2[Recall: 94.8%]
        A3[F1-Score: 95.5%]
        A4[Latencia: 1.8s]
        A5[Throughput: 33 fps]
    end
    
    subgraph FORECAST_METRICS["📈 Forecasting Performance"]
        F1[MAE: 3.2 espacios]
        F2[RMSE: 4.7 espacios]
        F3[R²: 0.89]
        F4[MAPE: 8.3%]
    end
    
    subgraph CHATBOT_METRICS["💬 Chatbot Performance"]
        C1[Intent Accuracy: 91.5%]
        C2[Response Time: 0.8s]
        C3[Self-Service: 78%]
        C4[User Satisfaction: 4.6/5]
    end
    
    subgraph OPTIMIZER_METRICS["🎯 Optimizer Performance"]
        O1[Tiempo Búsqueda: -42%]
        O2[Distancia: -35%]
        O3[Balance Carga: σ=12%]
        O4[User Happiness: +28%]
    end
    
    ALPR_METRICS -.Excelente.-> STATUS1[✅ Producción]
    FORECAST_METRICS -.Muy Bueno.-> STATUS2[✅ Producción]
    CHATBOT_METRICS -.Bueno.-> STATUS3[⚠️ Mejorando]
    OPTIMIZER_METRICS -.Excelente.-> STATUS4[✅ Producción]

    style A1 fill:#51cf66,color:#000
    style A2 fill:#51cf66,color:#000
    style A3 fill:#51cf66,color:#000
    style F1 fill:#4ecdc4,color:#000
    style F2 fill:#4ecdc4,color:#000
    style C1 fill:#ffd93d,color:#000
    style O1 fill:#51cf66,color:#000
```

---

## 🔄 Pipeline CI/CD para Modelos de IA

```mermaid
flowchart LR
    DEV[👨‍💻 Developer] --> GIT[Git Push<br/>GitHub]
    
    GIT --> TRIGGER{GitHub<br/>Actions}
    
    TRIGGER --> LINT[🔍 Linting<br/>Flake8/Black]
    TRIGGER --> TEST[🧪 Unit Tests<br/>Pytest]
    TRIGGER --> SECURITY[🔒 Security Scan<br/>Bandit]
    
    LINT --> BUILD{All Checks<br/>Pass?}
    TEST --> BUILD
    SECURITY --> BUILD
    
    BUILD -->|No| NOTIFY_FAIL[❌ Notificar<br/>Slack/Email]
    BUILD -->|Yes| DOCKER[🐳 Build Docker<br/>Image]
    
    DOCKER --> REGISTRY[📦 Push to<br/>Registry]
    
    REGISTRY --> STAGING[🔧 Deploy to<br/>Staging]
    
    STAGING --> AI_TEST[🤖 AI Model<br/>Validation]
    AI_TEST --> PERF_TEST[⚡ Performance<br/>Tests]
    
    PERF_TEST --> APPROVE{Manual<br/>Approval?}
    
    APPROVE -->|No| ROLLBACK[🔙 Rollback]
    APPROVE -->|Yes| PROD[🚀 Deploy to<br/>Production]
    
    PROD --> MONITOR[📊 Monitoring<br/>Grafana]
    MONITOR --> ALERT{Anomalías<br/>detectadas?}
    
    ALERT -->|Sí| ROLLBACK
    ALERT -->|No| SUCCESS[✅ Deployment<br/>Exitoso]
    
    ROLLBACK --> NOTIFY_FAIL
    SUCCESS --> NOTIFY_SUCCESS[✅ Notificar<br/>Éxito]

    style DEV fill:#74c0fc
    style SUCCESS fill:#51cf66,color:#000
    style NOTIFY_FAIL fill:#ff6b6b,color:#fff
    style PROD fill:#ffd93d
    style AI_TEST fill:#4ecdc4
```

---

## 🎓 Curva de Aprendizaje del Equipo

```mermaid
gantt
    title Capacitación y Curva de Aprendizaje
    dateFormat YYYY-MM-DD
    section ML Engineer
    Python Avanzado           :done, 2026-01-01, 20d
    Deep Learning             :done, 2026-01-15, 30d
    Computer Vision           :active, 2026-02-01, 40d
    MLOps                     :2026-03-01, 25d
    
    section Backend Dev
    Django Básico             :done, 2026-01-01, 15d
    Django REST Framework     :done, 2026-01-10, 20d
    Celery & Async            :active, 2026-02-01, 25d
    Performance Tuning        :2026-02-20, 20d
    
    section DevOps
    Docker Fundamentals       :done, 2026-01-01, 10d
    Kubernetes Basics         :active, 2026-01-15, 30d
    Monitoring Stack          :2026-02-10, 20d
    Security Best Practices   :2026-03-01, 15d
    
    section Data Scientist
    Estadística               :done, 2026-01-01, 25d
    Machine Learning          :active, 2026-01-20, 35d
    Time Series               :2026-02-15, 30d
    Feature Engineering       :2026-03-10, 20d
```

---

## 🏆 Resumen Ejecutivo Visual

```mermaid
graph TD
    TITLE[🚀 MoveTracker AI Transformation]
    
    subgraph PROBLEM["❌ PROBLEMA ACTUAL"]
        P1[Procesos manuales lentos]
        P2[Baja ocupación - 70%]
        P3[Experiencia usuario pobre]
        P4[Costos operativos altos]
    end
    
    subgraph SOLUTION["✅ SOLUCIÓN IA"]
        S1[🎥 ALPR Automático]
        S2[📈 Predicción ML]
        S3[🤖 Chatbot 24/7]
        S4[🎯 Optimización Espacios]
        S5[💰 Pricing Dinámico]
    end
    
    subgraph BENEFITS["💎 BENEFICIOS"]
        B1[⚡ 95% Automatización]
        B2[📊 85% Ocupación]
        B3[😊 4.6/5 Satisfacción]
        B4[💰 +20% Ingresos]
        B5[⏱️ ROI en 15 días]
    end
    
    subgraph TECH["🛠️ TECNOLOGÍA"]
        T1[YOLO v8]
        T2[PyTorch]
        T3[Django]
        T4[Redis]
        T5[Docker]
    end
    
    TITLE --> PROBLEM
    PROBLEM --> P1 & P2 & P3 & P4
    
    P1 --> S1
    P2 --> S2
    P3 --> S3
    P4 --> S4
    P4 --> S5
    
    S1 --> B1
    S2 --> B2
    S3 --> B3
    S4 --> B4
    S5 --> B5
    
    S1 --> T1
    S2 --> T2
    S3 --> T3
    S4 --> T4
    S5 --> T5

    style TITLE fill:#1864ab,color:#fff,stroke-width:4px
    style P1 fill:#ffc9c9,stroke:#c92a2a
    style P2 fill:#ffc9c9,stroke:#c92a2a
    style P3 fill:#ffc9c9,stroke:#c92a2a
    style P4 fill:#ffc9c9,stroke:#c92a2a
    style S1 fill:#74c0fc,stroke:#1864ab
    style S2 fill:#74c0fc,stroke:#1864ab
    style S3 fill:#74c0fc,stroke:#1864ab
    style S4 fill:#74c0fc,stroke:#1864ab
    style S5 fill:#74c0fc,stroke:#1864ab
    style B1 fill:#51cf66,stroke:#2f9e44
    style B2 fill:#51cf66,stroke:#2f9e44
    style B3 fill:#51cf66,stroke:#2f9e44
    style B4 fill:#51cf66,stroke:#2f9e44
    style B5 fill:#ffd93d,stroke:#f59f00
```

---

## 📋 Conclusión de Visualizaciones

Este documento complementa los otros materiales de investigación con representaciones visuales adicionales que cubren:

1. ✅ **Flujos de proceso detallados** - Secuencias y estados
2. ✅ **Arquitecturas técnicas** - Capas y componentes
3. ✅ **Métricas y KPIs** - Dashboards conceptuales
4. ✅ **Comparativas** - Antes vs después
5. ✅ **Seguridad y privacidad** - Capas de protección
6. ✅ **Mobile y apps** - Experiencia usuario
7. ✅ **CI/CD y DevOps** - Procesos de despliegue
8. ✅ **Aprendizaje del equipo** - Capacitación

### 📚 Documentos Relacionados:
- `AI_RESEARCH.md` - Investigación técnica detallada
- `CONCEPTUAL_MAP.md` - Mapas conceptuales principales
- `IDEA_ORGANIZER.md` - Planificación y organización

---

**Generado:** 25 de Octubre, 2025  
**Versión:** 1.0  
**Formato:** Mermaid Diagrams para visualización interactiva
