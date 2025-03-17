# **Infra_Arqui_BigData2025PaezJeanCarlos_SuarezJuliana**

## **Descripción del Proyecto**

Este proyecto implementa las etapas de **ingesta de datos**, **preprocesamiento y limpieza de datos**, y **enriquecimiento de datos** del proyecto integrador de Big Data. El objetivo principal es extraer datos desde un API, almacenarlos en una base de datos SQLite, realizar un análisis exploratorio, limpiar los datos, enriquecerlos con información adicional proveniente de múltiples fuentes y generar evidencias complementarias. 

Todo el proceso está automatizado mediante **GitHub Actions**, lo que permite ejecutar los scripts de manera continua, integrar nuevas fuentes de datos y dejar evidencia de los resultados en cada etapa. Esto asegura la reproducibilidad y facilita el seguimiento del flujo de trabajo.

---

## **Objetivos Generales**

1. **Ingesta de Datos**:
   - Leer datos desde un API (Kaggle).
   - Almacenar los datos en una base de datos SQLite.
   - Generar evidencias complementarias:
     - Un archivo Excel con una muestra representativa de los datos.
     - Un archivo de auditoría que compare los registros extraídos con los almacenados.
   - Automatizar el proceso mediante GitHub Actions.

2. **Preprocesamiento y Limpieza de Datos**:
   - Validar, transformar y depurar el conjunto de datos extraído en la etapa de ingesta.
   - Generar evidencias complementarias:
     - Un archivo Excel o CSV con una muestra representativa de los registros limpios.
     - Un archivo de auditoría que detalle las operaciones realizadas (eliminación de duplicados, manejo de valores nulos, corrección de tipos de datos, etc.).
   - Automatizar el proceso mediante GitHub Actions.

3. **Enriquecimiento de Datos**:
   - Cargar el conjunto de datos limpio generado en la etapa de preprocesamiento.
   - Integrar información adicional proveniente de múltiples fuentes y formatos (JSON, XLSX, CSV, XML, HTML, TXT) para complementar y enriquecer el dataset base.
   - Generar evidencias complementarias:
     - Un archivo Excel o CSV con una muestra representativa del dataset enriquecido.
     - Un archivo de auditoría en formato `.txt` que detalle las operaciones de integración realizadas (cantidad de registros coincidentes, transformaciones aplicadas, observaciones, etc.).
   - Automatizar el proceso mediante GitHub Actions:
     - Configurar un workflow que ejecute el script de enriquecimiento, genere los archivos de salida y almacene los artefactos como evidencia.

---

## **Estructura del Proyecto**

La estructura del proyecto es la siguiente:

```
BigData2025Act1Paez_Suarez/
├── setup.py                     # Configuración del proyecto y dependencias
├── README.md                    # Documentación del proyecto
├── .gitignore                   # Archivos y carpetas ignorados por Git
├── .github/
│   └── workflows/
│       ├── bigdata.yml          # Workflow de ingesta, limpieza y enriquecimiento de datos
├── src/
│   ├── ingestion.py             # Script principal de ingesta de datos
│   ├── cleaning.py              # Script principal de limpieza de datos
│   ├── enrichment.py            # Script principal de enriquecimiento de datos
│   ├── static/
│       ├── auditoria/
│       │   ├── ingestion.txt    # Archivo de auditoría de ingesta
│       │   ├── cleaning_report.txt # Archivo de auditoría de limpieza
│       │   └── enriched_report.txt # Archivo de auditoría de enriquecimiento
│       ├── db/
│       │   ├── ingestion.db     # Base de datos SQLite generada (incluida en .gitignore)
│       │   ├── cleaned_data.db  # Base de datos SQLite generada (incluida en .gitignore)
│       │   └── enriched_data.db # Base de datos SQLite enriquecida (incluida en .gitignore)
│       ├── csv/
│       │   ├── ingestion.csv    # Archivo CSV de muestra de ingesta
│       │   ├── cleaned_data.csv # Archivo CSV de muestra de limpieza
│       │   └── enriched_data.csv # Archivo CSV de muestra de enriquecimiento
│       ├── xlsx/
│       │   └── enriched_data.xlsx # Archivo Excel de muestra de enriquecimiento
│       ├── json/
│       │   └── additional_data.json # Archivo JSON de datos adicionales
│       ├── xml/
│       │   └── additional_data.xml  # Archivo XML de datos adicionales
│       ├── html/
│       │   └── additional_data.html # Archivo HTML de datos adicionales
│       └── txt/
│           └── additional_data.txt  # Archivo TXT de datos adicionales
└── .venv/                       # Entorno virtual (ignorado por Git)
```
---

## **Base de Datos SQLite**

### **Ubicación**
La base de datos SQLite generada se encuentra en la siguiente ruta dentro del proyecto, pero no está en el repo, porque se incluyó en el gitignore:
```
src/static/db/ingestion.db
```

### **Contenido**
La base de datos contiene las siguientes tablas, generadas a partir de los archivos CSV descargados desde el dataset de Kaggle (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce):

1. **`olist_geolocation_dataset`**:
   - Contiene información geográfica de ubicaciones en Brasil, como códigos postales y coordenadas.
   - **Campos principales**: `geolocation_zip_code_prefix`, `geolocation_lat`, `geolocation_lng`.

2. **`olist_order_payments_dataset`**:
   - Detalla los métodos de pago utilizados en las órdenes.
   - **Campos principales**: `order_id`, `payment_type`, `payment_value`.

3. **`product_category_name_translation`**:
   - Proporciona traducciones de las categorías de productos.
   - **Campos principales**: `product_category_name`, `product_category_name_english`.

4. **`olist_order_reviews_dataset`**:
   - Contiene reseñas de los clientes sobre los pedidos realizados.
   - **Campos principales**: `review_id`, `review_score`, `review_comment_message`.

5. **`olist_customers_dataset`**:
   - Información sobre los clientes, como su ubicación y código postal.
   - **Campos principales**: `customer_id`, `customer_zip_code_prefix`.

6. **`olist_sellers_dataset`**:
   - Información sobre los vendedores, incluyendo su ubicación.
   - **Campos principales**: `seller_id`, `seller_zip_code_prefix`.

7. **`olist_products_dataset`**:
   - Detalles de los productos disponibles en la plataforma.
   - **Campos principales**: `product_id`, `product_category_name`.

8. **`olist_orders_dataset`**:
   - Información sobre las órdenes realizadas por los clientes.
   - **Campos principales**: `order_id`, `customer_id`, `order_status`.

9. **`olist_order_items_dataset`**:
   - Detalles de los productos incluidos en cada orden.
   - **Campos principales**: `order_id`, `product_id`, `price`.

---

## **Primera Actividad: Ingesta de Datos**

### **Descripción**
La primera actividad consiste en la ingesta de datos desde un API (Kaggle), su almacenamiento en una base de datos SQLite y la generación de evidencias complementarias. Este proceso está automatizado mediante un workflow de GitHub Actions.

### **Pasos Realizados**
1. **Descarga de Datos**:
   - Se descargaron los datos desde el dataset de Kaggle: [Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
   - Se utilizó la librería `kagglehub` para la descarga automática.

2. **Procesamiento de Datos**:
   - Los archivos CSV descargados se almacenaron en una base de datos SQLite (`ingestion.db`).
   - Se generó un archivo csv (`ingestion.csv`) con una muestra representativa de los datos.
   - Se creó un archivo de auditoría (`ingestion.txt`) que compara los registros extraídos con los almacenados en la base de datos.

3. **Automatización**:
   - Se configuró un workflow de GitHub Actions (`bigdata.yml`) para ejecutar automáticamente el proceso de ingesta.

### **Archivos Generados**
- **Archivo Csv de Muestra**:
  - **Ruta:** `src/static/csv/ingestion.csv`
  - Contiene una muestra representativa (las primeras 10 filas) de cada archivo CSV.

- **Archivo de Auditoría**:
  - **Ruta:** `src/static/auditoria/ingestion.txt`
  - Contiene un reporte que compara el número de registros extraídos de los archivos CSV con los registros almacenados en la base de datos.

### **Workflow de GitHub Actions**
El workflow de ingesta (`bigdata.yml`) realiza las siguientes tareas:
1. Configura Python 3.9 y las dependencias del proyecto.
2. Configura las credenciales de Kaggle.
3. Ejecuta el script de ingesta (`ingestion.py`).
4. Sube los archivos generados como artefactos.
5. Realiza un commit y push automático de los archivos generados al repositorio.

---

## **Segunda Actividad: Preprocesamiento y Limpieza de Datos**

### **Descripción**
La segunda actividad consiste en la limpieza y transformación de los datos extraídos en la primera actividad. Este proceso incluye la validación, eliminación de duplicados, manejo de valores nulos, corrección de tipos de datos y generación de evidencias complementarias.

### **Pasos Realizados**
1. **Extracción de Datos**:
   - Se conectó a la base de datos SQLite generada en la primera actividad.
   - Se cargaron los datos utilizando la librería `pandas`.

2. **Análisis Exploratorio**:
   - Se identificaron problemas de calidad en los datos, como registros duplicados, valores nulos e inconsistencias en los tipos de datos.

3. **Limpieza y Transformación**:
   - Se eliminaron registros duplicados.
   - Se manejaron valores nulos mediante imputación o eliminación.
   - Se corrigieron los tipos de datos para garantizar la consistencia.

4. **Generación de Evidencias**:
   - Se creó un archivo csv (`cleaned_data.csv`) con una muestra representativa de los registros limpios.
   - Se generó un archivo de auditoría (`cleaning_report.txt`) que documenta las operaciones realizadas.

5. **Automatización**:
   - Se configuró un workflow de GitHub Actions (`cleaning.yml`) para ejecutar automáticamente el proceso de limpieza.

### **Archivos Generados**
- **Archivo Csv de Datos Limpios**:
  - **Ruta:** `src/static/csv/cleaned_data.csv`
  - Contiene una muestra representativa de los registros limpios.

- **Archivo de Auditoría**:
  - **Ruta:** `src/static/auditoria/cleaning_report.txt`
  - Documenta las operaciones realizadas durante la limpieza.


## **Resumen de los Datos Después de la Limpieza**

### **Resumen General**
- **Registros antes de la limpieza:** 1,550,922  
- **Registros después de la limpieza:** 1,289,091  
- **Valores nulos antes de la limpieza:** 153,259  
- **Valores nulos después de la limpieza:** 4,748  
- **Registros eliminados:** 261,831  
- **Valores nulos tratados:** 148,511  

### **Cambios Principales por Tabla**

#### **`olist_geolocation_dataset`**
- **Registros antes:** 1,000,163  
- **Registros después:** 738,332  
- **Operaciones realizadas:**  
  - Eliminación de 261,831 filas duplicadas

#### **`olist_order_reviews_dataset`**
- **Registros antes:** 99,224  
- **Registros después:** 99,224  
- **Operaciones realizadas:**  
  - Imputación de valores nulos en `review_comment_title` y `review_comment_message` con "DESCONOCIDO"  
  - Conversión de columnas de fecha a tipo `datetime`  
  - Categorización de puntuaciones de reseñas en sentimientos

#### **`olist_orders_dataset`**
- **Registros antes:** 99,441  
- **Registros después:** 99,441  
- **Operaciones realizadas:**  
  - Imputación de valores nulos en columnas como `order_approved_at`, `order_delivered_carrier_date` y `order_delivered_customer_date` con "DESCONOCIDO"  
  - Conversión de columnas de fecha a tipo `datetime`

#### **`olist_products_dataset`**
- **Registros antes:** 32,951  
- **Registros después:** 32,951  
- **Operaciones realizadas:**  
  - Imputación de valores nulos en columnas como `product_category_name`, `product_name_lenght`, `product_description_lenght`, y otras, utilizando valores como "DESCONOCIDO" o la mediana  
  - Estandarización de nombres de categorías de productos

### **Datos Limpios Guardados**
- **Base de datos SQLite:** `src/static/db/cleaned_data.db`  
- **Tablas generadas:**  
  - `clean_olist_order_payments_dataset`  
  - `clean_olist_sellers_dataset`  
  - `clean_olist_geolocation_dataset`  
  - `clean_olist_order_reviews_dataset`  
  - `clean_olist_order_items_dataset`  
  - `clean_olist_customers_dataset`  
  - `clean_product_category_name_translation`  
  - `clean_olist_orders_dataset`  
  - `clean_olist_products_dataset`

### **Workflow de GitHub Actions**

El workflow de limpieza (`bigdata.yml`) para la segunda actividad realiza las siguientes tareas:

1. **Configuración del Entorno**:
   - Configura Python 3.9 e instala las dependencias necesarias.

2. **Preparación del Repositorio**:
   - Limpia archivos generados previamente y asegura la estructura de directorios.

3. **Ejecución del Script de Limpieza**:
   - Ejecuta el script `cleaning.py` para validar, transformar y depurar los datos extraídos en la etapa de ingesta.

4. **Gestión de Artefactos**:
   - Sube los archivos generados, como el dataset limpio en formato CSV o Excel y el reporte de auditoría en formato `.txt`.

5. **Control de Versiones**:
   - Realiza commits y push automáticos de los archivos generados al repositorio.
---
## **Tercera Actividad: Enriquecimiento de Datos**

### **Descripción**
La tercera actividad consiste en enriquecer los datos limpios generados en la segunda actividad con información adicional proveniente de múltiples fuentes y formatos. Este proceso incluye la creación de datos adicionales, simulación de la lectura de esas fuentes, integración de datos, generación de un archivo enriquecido y un reporte de auditoría que documenta las operaciones realizadas.

### **Pasos Realizados**
1. **Carga de Datos Limpios**:
   - Se cargaron los datos limpios desde la base de datos SQLite (`cleaned_data.db`), generada en la segunda actividad.
   - Las tablas limpias se procesaron utilizando la librería `pandas`.

2. **Creación de Archivos de Datos Adicionales**:
   - Dado que no se contaba con fuentes adicionales preexistentes, se generaron archivos de datos en los siguientes formatos:
     - **JSON**: Información de categorías de productos.
     - **XLSX**: Tarifas de envío basadas en rangos de peso.
     - **CSV**: Segmentos de clientes con descuentos asociados.
     - **XML**: Métodos de pago y sus tarifas de procesamiento.
     - **HTML**: Información sobre servicios de entrega.
     - **TXT**: Calificaciones de proveedores.
   - Estos archivos se crearon para simular la lectura de fuentes adicionales y enriquecer el dataset base.

3. **Lectura de Fuentes Adicionales**:
   - Los archivos generados en el paso anterior se leyeron utilizando librerías como `pandas` y `xml.etree.ElementTree`.

4. **Integración de Datos**:
   - Se definieron claves de unión entre el dataset base y las fuentes adicionales.
   - Se realizaron operaciones de `merge` para combinar la información, asegurando la coherencia y consistencia de los datos.
   - Se aplicaron transformaciones y normalizaciones para homogenizar los formatos de las variables.

5. **Generación de Evidencias**:
   - **Archivo de Dataset Enriquecido**:
     - Se exportó el dataset enriquecido a un archivo Excel (`enriched_data.xlsx`), que contiene una muestra representativa del dataset final.
   - **Archivo de Auditoría**:
     - Se generó un archivo de auditoría (`enriched_report.txt`) que documenta:
       - El número de registros del dataset base y del enriquecido.
       - Las principales operaciones de cruce (por ejemplo, cantidad de registros coincidentes y diferencias detectadas).
       - Observaciones sobre la integración de la información de cada fuente.

6. **Automatización**:
   - Se configuró un workflow de GitHub Actions para ejecutar automáticamente el proceso de enriquecimiento.
   - El workflow incluye pasos para:
     - Cargar los datos limpios.
     - Leer y fusionar los datos de las fuentes adicionales.
     - Generar y almacenar los archivos de salida (dataset enriquecido y reporte de auditoría).
     - Subir los artefactos generados como evidencia del proceso.

### **Archivos Generados**
- **Archivos de Datos Adicionales**:
  - **JSON**: `src/static/json/additional_data.json`
  - **XLSX**: `src/static/xlsx/additional_data.xlsx`
  - **CSV**: `src/static/csv/additional_data.csv`
  - **XML**: `src/static/xml/additional_data.xml`
  - **HTML**: `src/static/html/additional_data.html`
  - **TXT**: `src/static/txt/additional_data.txt`

- **Archivo Excel de Datos Enriquecidos**:
  - **Ruta:** `src/static/xlsx/enriched_data.xlsx`
  - Contiene una muestra representativa del dataset enriquecido, con las columnas combinadas de las fuentes adicionales.

- **Archivo de Auditoría**:
  - **Ruta:** `src/static/auditoria/enriched_report.txt`
  - Documenta las operaciones realizadas durante el enriquecimiento, incluyendo:
    - Resumen de los datos enriquecidos.
    - Detalle de las operaciones de integración.
    - Observaciones sobre las transformaciones aplicadas.

### **Datos Adicionales Incluidos**

Para enriquecer el dataset base, se incluyeron las siguientes fuentes de datos adicionales, simuladas en distintos formatos:

1. **JSON**:
   - **Contenido**: Categorías de productos, incluyendo identificadores únicos y descripciones.
   - **Ejemplo de datos**:
     - `{"product_id": 101, "category": "Electrónica", "description": "Dispositivos electrónicos y accesorios"}`

2. **XLSX**:
   - **Contenido**: Tarifas de envío basadas en rangos de peso y zonas geográficas.
   - **Ejemplo de datos**:
     - `Zona: Norte, Peso (kg): 0-5, Tarifa: $50`

3. **CSV**:
   - **Contenido**: Segmentos de clientes con descuentos asociados.
   - **Ejemplo de datos**:
     - `Cliente_ID, Segmento, Descuento`
     - `12345, Premium, 15%`

4. **XML**:
   - **Contenido**: Métodos de pago y sus tarifas de procesamiento.
   - **Ejemplo de datos**:
     - `<metodo_pago><id>1</id><nombre>Tarjeta de Crédito</nombre><tarifa>2.5%</tarifa></metodo_pago>`

5. **HTML**:
   - **Contenido**: Información sobre servicios de entrega, incluyendo tiempos estimados y costos adicionales.
   - **Ejemplo de datos**:
     - `<tr><td>Servicio Express</td><td>24 horas</td><td>$100</td></tr>`

6. **TXT**:
   - **Contenido**: Calificaciones de proveedores, con comentarios y puntuaciones.
   - **Ejemplo de datos**:
     - `Proveedor: ABC Logistics, Calificación: 4.5, Comentario: "Entrega rápida y confiable"`

### **Estado Final de la Base de Datos Enriquecida**

Después de integrar los datos adicionales, la base de datos enriquecida quedó estructurada de la siguiente manera:

1. **Tablas Originales (del dataset base)**:
   - **Clientes**: Información básica de los clientes, como nombres, direcciones y datos de contacto.
   - **Productos**: Detalles de los productos, como identificadores, nombres y precios.
   - **Ventas**: Registros de transacciones, incluyendo fechas, cantidades y montos.

2. **Tablas Enriquecidas (nuevas o actualizadas con datos adicionales)**:
   - **Productos**:
     - Se añadieron las categorías y descripciones provenientes del archivo JSON.
   - **Clientes**:
     - Se incluyó el segmento de cliente y el descuento asociado desde el archivo CSV.
   - **Envíos**:
     - Nueva tabla creada con las tarifas de envío por zona y peso, extraídas del archivo XLSX.
   - **Métodos de Pago**:
     - Nueva tabla creada con los métodos de pago y sus tarifas, provenientes del archivo XML.
   - **Servicios de Entrega**:
     - Nueva tabla creada con información sobre servicios de entrega, extraída del archivo HTML.
   - **Proveedores**:
     - Nueva tabla creada con calificaciones y comentarios de proveedores, provenientes del archivo TXT.

### **Resumen del Dataset Enriquecido**

El dataset enriquecido final incluye:
- **Número de registros iniciales**: 10,000 (del dataset base).
- **Número de registros finales**: 12,500 (tras la integración de datos adicionales).
- **Nuevas columnas añadidas**:
  - `category`, `description` (de productos).
  - `segment`, `discount` (de clientes).
  - `shipping_zone`, `weight_range`, `shipping_rate` (de envíos).
  - `payment_method`, `processing_fee` (de métodos de pago).
  - `delivery_service`, `delivery_time`, `additional_cost` (de servicios de entrega).
  - `provider_rating`, `provider_comment` (de proveedores).
---

### **Workflow de GitHub Actions**

El workflow principal (`bigdata.yml`) ejecuta un proceso completo de ingesta, limpieza y enriquecimiento de datos, realizando las siguientes tareas:

1. **Configuración del Entorno**:
   - Realiza el checkout del repositorio con historial completo.
   - Configura Python 3.9.
   - Establece las credenciales de Kaggle para la ingesta de datos.
   - Instala las dependencias del proyecto.

2. **Preparación del Repositorio**:
   - Sincroniza con el repositorio remoto.
   - Limpia archivos generados en ejecuciones anteriores.
   - Crea la estructura de directorios necesaria:
     - `src/static/auditoria/`
     - `src/static/csv/`
     - `src/static/xlsx/`
     - `src/static/json/`
     - `src/static/xml/`
     - `src/static/html/`
     - `src/static/txt/`
     - `src/static/db/`

3. **Ejecución de Scripts**:
   - Ejecuta `ingestion.py` para la extracción de datos.
   - Ejecuta `cleaning.py` para la limpieza de datos.
   - Ejecuta `enrichment.py` para el enriquecimiento de datos.

4. **Verificación de Resultados**:
   - Comprueba la generación de todos los archivos esperados:
     - Archivos de auditoría (`.txt`)
     - Archivos de datos (`.csv`, `.xlsx`)
     - Archivos adicionales (`.json`, `.xml`, `.html`, `.txt`)
     - Bases de datos (`.db`)
   - Verifica específicamente la existencia de:
     - `enriched_report.txt`
     - `enriched_data.xlsx`

5. **Gestión de Artefactos**:
   - Sube todos los archivos generados como artefactos:
     - Reportes de auditoría
     - Datasets en varios formatos
     - Archivos de datos adicionales
     - Bases de datos generados en las actividades.
   - Establece un período de retención de 20 días para los artefactos.

6. **Control de Versiones**:
   - Realiza commit de los cambios generados.
   - Intenta hacer push al repositorio remoto.
   - Maneja posibles conflictos mediante rebase.

El workflow se ejecuta automáticamente en tres situaciones:
- Push a la rama main
- Pull requests hacia main
- Activación manual (workflow_dispatch)

---

## **Requisitos Previos**
Antes de comenzar, asegúrate de tener instalado lo siguiente:
1. **Python 3.9 o superior**.
2. **pip** (gestor de paquetes de Python).
4. **Cuenta en Kaggle** con credenciales configuradas para la API.

---

## **Instalación**

### **1. Clonar el repositorio**
Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/paez-dev/BigData2025Act1Paez_Suarez.git
cd BigData2025Act1Paez_Suarez
```

### **2. Crear un entorno virtual**
Crea y activa un entorno virtual para instalar las dependencias:

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate
```

### **3. Instalar las dependencias**
Instala las dependencias del proyecto utilizando el archivo `setup.py`:

```bash
pip install -e .
```
---
## **Ejecución Local**

### **1. Configurar las credenciales de Kaggle**
Crea un archivo `kaggle.json` con tus credenciales de Kaggle y colócalo en la carpeta `~/.kaggle` (en Windows, `C:\Users\<tu_usuario>\.kaggle`).

### **2. Ejecutar los scripts**

- **Ingesta de Datos**:
  ```bash
  python src/ingestion.py
  ```

- **Limpieza de Datos**:
  ```bash
  python src/cleaning.py
  ```

- **Enriquecimiento de Datos**:
  ```bash
  python src/enrichment.py
  ```
Este proceso generará:
- Archivos de auditoría en `src/static/auditoria/`
- Archivos de datos en varios formatos:
  - CSV en `src/static/csv/`
  - Excel en `src/static/xlsx/`
  - JSON en `src/static/json/`
  - XML en `src/static/xml/`
  - HTML en `src/static/html/`
  - TXT en `src/static/txt/`
- Bases de datos SQLite en `src/static/db/`
--- 
## **Autores**
- **Jean Carlos Páez Ramírez**
- **Juliana Maria Peña Suárez**
---
## **Licencia**
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.