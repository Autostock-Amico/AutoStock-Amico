AutoStock — Sistema de Control de Inventario y Reportes para Comercios

1. Definición Inicial y Objetivo Principal
AutoStock es una aplicación web de gestión interna orientada a vendedores y encargados de depósito. Su objetivo principal es optimizar la administración de productos, automatizar el control de entradas y salidas de stock, generar alertas visuales de reposición para artículos en nivel crítico y emitir reportes exportables en formatos PDF y Excel.

2. Límites del Sistema (Scope Boundary)
Dentro del Alcance
Sistema de uso exclusivo para el personal del comercio (vendedores/administradores).
Autenticación de usuarios mediante tokens JWT.
CRUD completo de productos y categorías.
Registro de movimientos de stock (entradas por compras, salidas por ventas).
Sistema de alertas visuales automáticas cuando el stock actual sea menor o igual al stock mínimo.
Exportación de reportes de inventario en formato Excel (.xlsx).
Generación de informes impresos/descargables en formato PDF (.pdf).
Despliegue de la base de datos en un contenedor Docker con persistencia de datos (volúmenes).
Implementación redundante de la API en 2 frameworks Backend distintos (Express y FastAPI).
Implementación redundante del cliente web en 2 frameworks Frontend distintos (React y Vue 3).
Fuera del Alcance
Portal o vista pública para clientes finales / e-commerce.
Integración con entes impositivos o facturación electrónica (AFIP, etc.).
Lectura automática de código de barras mediante cámara web o hardware lector.
Procesamiento de pagos reales o pasarelas de pago (Mercado Pago, Stripe, etc.).
Notificaciones por correo electrónico, WhatsApp o SMS.


3. Alcances Funcionales y No Funcionales
Alcances Funcionales
Autenticación y Gestión de Sesiones: El vendedor puede registrarse e iniciar sesión de forma segura. El sistema emite un token JWT que permite acceder a las rutas protegidas.
Alta, Lectura, Edición y Baja de Productos: Permite al vendedor registrar nuevos productos (con campos: nombre, SKU/código, categoría, precio de costo, precio de venta, stock actual y stock mínimo), consultar el catálogo general, modificar sus datos o eliminarlos.
Búsqueda por SKU/Nombre y Filtros por Categoría: Motor de búsqueda interactivo en el cliente que permite filtrar productos por su código SKU, coincidencia de nombre o por categoría asignada.
Control de Entradas y Salidas de Stock: Módulo para registrar incrementos de mercadería (compras a proveedores) o descuentos rápidos de inventario (ventas realizadas en mostrador) sobre un producto seleccionado.
Identificación y Alertas de Stock Crítico: Mecanismo automático que compara el stock actual contra el stock mínimo configurado. Muestra etiquetas visuales destacadas en rojo/amarillo y ofrece una vista filtrada con los productos que requieren reposición.
Generación y Descarga de Planillas Excel: Funcionalidad para procesar la lista de productos (completa o filtrada) y descargar un archivo estructurado en formato .xlsx.
Emisión de Informes de Inventario en PDF: Módulo para generar un documento impreso o descargable en formato .pdf con el estado del inventario, métricas de valorización total (costo vs. venta) y la lista de reposición urgente.
Alcances No Funcionales
Encriptación y Control de Accesos: Hasheado obligatorio de contraseñas utilizando el algoritmo bcrypt en la base de datos y validación de tokens JWT en las cabeceras HTTP de la API.
Contenedorización de MongoDB con Volúmenes: Despliegue de la base de datos mediante Docker Compose, configurando volúmenes de datos montados en el host para garantizar la persistencia tras reinicios o caídas del contenedor.
Latencia de Endpoints REST: Los endpoints de la API para operaciones CRUD estándar deben responder con un tiempo de latencia inferior a 200 milisegundos bajo carga de trabajo normal.
Interfaz Adaptable y Tiempos de Respuesta Visual: Diseño adaptable (Responsive) orientado a paneles de administración desktop/tablet, ofreciendo feedback visual inmediato (notificaciones, confirmaciones y spinners de carga) en menos de 100 milisegundos.
Homogeneidad entre Backends y Frontends: Estricta compatibilidad y simetría en los contratos JSON, endpoints REST, códigos de respuesta HTTP y vistas de usuario entre ambas versiones de Backend (Express y FastAPI) y ambas de Frontend (React y Vue 3)

4. Objetivos Específicos y Medibles (SMART)
Paridad de Backend (100%): Desarrollar la API REST completa con autenticación, CRUD, lógica de stock y exportación de archivos tanto en Express (Node.js) como en FastAPI (Python), asegurando que ambas versiones compartan la misma estructura de respuestas y endpoints.
Paridad de Frontend (100%): Implementar la interfaz de administración completa tanto en React como en Vue.js 3, manteniendo idénticas vistas, flujos de navegación, validaciones y consumo de la API.
Persistencia Dockerizada: Configurar un archivo docker-compose.yml que levante el motor MongoDB con volúmenes persistentes en menos de 2 minutos mediante el comando docker-compose up.
Exportación de Datos: Garantizar la correcta generación de reportes descargables (archivos válidos .pdf y .xlsx) desde ambos backends en menos de 3 segundos para catálogos de hasta 1,000 productos.
Calidad de Código y Flujo Git: Registrar el 100% de los cambios mediante el flujo de ramas, Pull Requests aprobados por el docente y mensajes de commit bajo la convención Conventional Commits.

