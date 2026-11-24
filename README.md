# ViaSOS - Proyecto de Seguridad y Asistencia

**Asignatura:** Proyecto Integrado (Sección: TIHV43)  
**Docente:** Francisco Andrés Iturra Piceros  
**Integrantes:** 
- Joshua Ulloa Oliva (Scrum Master)
- Neftali Garcia  (Product Owner)
- Armando Morales  (Equipo de Desarrollo)
- Roberto Araya  (Equipo de Desarrollo)


##  Descripción del Proyecto
ViaSOS es una plataforma web diseñada para facilitar el acceso a información crítica de una persona en situaciones de emergencia. A trasvés de códigos QR vinculados a una "ficha de auxilio", cualquier persona puede consultar los datos que el titular haya autorizado compartir, sin necesidad de instalar aplicaciones ni iniciar sesión.

El objetivo principal es proporcionar una herramienta rápida, confiable y accesible para quienes necesitan ayudar en momentos críticos.


##  Estado del Proyecto (Etapa 2)
Actualmente, el proyecto se encuentra en su segunda etapa de desarrollo, enfocada en la consolidación técnica del Producto Mínimo Viable (MVP). Se ha avanzado en:
- Planificación mediante metodología ágil **Scrum** (Sprints definidos).
- Definición de la arquitectura del sistema (Modelo 4+1).
- Diseño del prototipo funcional y flujos de usuario.
- Estructuración de la base de datos NoSQL (MongoDB).
- Definición de políticas de seguridad y control de acceso.


##  Tecnologías Utilizadas

| Componente | Tecnología |
| :--- | :--- |
| **Frontend** | HTML, CSS y JavaScript |
| **Backend** | Python y Django |
| **Base de Datos** | MongoDB (NoSQL) |
| **Conector DB** | PyMongo |
| **Administración DB**| MongoDB Compass |
| **Control de Versiones**| Git y GitHub |
| **Editor de Código** | Visual Studio Code |



## 🏗️ Arquitectura del Sistema
El sistema se rige bajo el patrón **Modelo-Vista-Controlador (MVC)**, adaptado al patrón **MVT (Modelo-Vista-Plantilla)** nativo de Django:
1. **Modelo:** Gestión de datos y comunicación con MongoDB (vía PyMongo).
2. **Vista:** Interfaz de usuario desarrollada con HTML/CSS/JS.
3. **Controlador:** Lógica de negocio y procesamiento de solicitudes en Django.

### Vistas del Sistema (Paradigma 4+1)
- **Vista Lógica:** Diagrama de clases con entidades como Usuario, Perfil, Contactos, QR, Soporte, Notificaciones y Preguntas.
- **Vista de Desarrollo:** Separación de componentes Frontend (vistas pública/privada) y Backend (autenticación, lógica de negocio, PyMongo).
- **Vista de Procesos:** Flujos de consulta pública por QR y administración privada del perfil.
- **Vista Física:** Despliegue en servidor web (Freehost.cl) y base de datos MongoDB.



##  Seguridad y Privacidad
ViaSOS prioriza la protección de datos:
- **Consulta Pública:** Solo muestra información explícitamente autorizada por el usuario.
- **Autenticación:** Gestión segura de sesiones y contraseñas para el acceso al panel privado.
- **Códigos QR:** Los usuarios pueden suspender o desvincular sus etiquetas QR en cualquier momento.


git clone https://github.com/JoshMuo/Proyecto-Integrado-Viasos.git
python -m venv .venv
.venv\Scripts\activate
python manage.py runserver
