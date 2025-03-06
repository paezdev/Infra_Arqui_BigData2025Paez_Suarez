# **Infra_Arqui_BigData2025PaezJeanCarlos_SuarezJuliana**

## **Descripción del Proyecto**
Este proyecto implementa las etapas de **ingesta de datos** y **preprocesamiento y limpieza de datos** del proyecto integrador de Big Data. El objetivo principal es extraer datos desde un API, almacenarlos en una base de datos SQLite, realizar un análisis exploratorio, limpiar los datos y generar evidencias complementarias. Todo el proceso está automatizado mediante **GitHub Actions**, lo que permite ejecutar los scripts de manera continua y dejar evidencia de los resultados.

---

## **Objetivos Generales**
1. **Ingesta de Datos**:
   - Leer datos desde un API (Kaggle).
   - Almacenar los datos en una base de datos SQLite.
   - Generar evidencias complementarias:
     - Un archivo Excel con una muestra representativa de los datos.
     - Un archivo de auditoría que compare los registros extraídos con los almacenados.
   - Automatizar el proceso mediante GitHub Actions.
   - Manejar archivos pesados (como la base de datos) utilizando **Git LFS**.

2. **Preprocesamiento y Limpieza de Datos**:
   - Validar, transformar y depurar el conjunto de datos extraído en la etapa de ingesta.
   - Generar evidencias complementarias:
     - Un archivo Excel o CSV con una muestra representativa de los registros limpios.
     - Un archivo de auditoría que detalle las operaciones realizadas (eliminación de duplicados, manejo de valores nulos, corrección de tipos de datos, etc.).
   - Automatizar el proceso mediante GitHub Actions.

---

## **Estructura del Proyecto**
La estructura del proyecto es la siguiente:

```
Infra_Arqui_BigData2025Paez_Suarez/
├── setup.py                     # Configuración del proyecto y dependencias
├── README.md                    # Documentación del proyecto
├── .gitattributes               # Configuración de Git LFS para archivos pesados
├── .gitignore                   # Archivos y carpetas ignorados por Git
├── .github/
│   └── workflows/
│       ├── bigdata.yml          # Workflow de ingesta de datos
├── src/
│   ├── ingestion.py             # Script principal de ingesta de datos
│   ├── cleaning.py              # Script principal de limpieza de datos
│   ├── static/
│       ├── auditoria/
│       │   ├── ingestion.txt    # Archivo de auditoría de ingesta
│       │   └── cleaning_report.txt # Archivo de auditoría de limpieza
│       ├── db/
│       │   └── ingestion.db     # Base de datos SQLite generada (manejada con Git LFS)
│       └── csv/
│           ├── ingestion.csv   # Archivo csv de muestra de ingesta
│           └── cleaned_data.csv # Archivo csv de muestra de limpieza
└── .venv/                       # Entorno virtual (ignorado por Git)
```

## **Base de Datos SQLite**

### **Ubicación**
La base de datos SQLite generada se encuentra en la siguiente ruta dentro del proyecto:
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
- **Base de Datos SQLite**:
  - **Ruta:** `src/static/db/ingestion.db`
  - Contiene las tablas generadas a partir de los archivos CSV descargados.
  - **Nota:** Este archivo es manejado mediante **Git LFS** debido a su tamaño.

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

### **Workflow de GitHub Actions**
El workflow de limpieza (`cleaning.yml`) realiza las siguientes tareas:
1. Configura Python 3.9 y las dependencias del proyecto.
2. Extrae los datos desde la base de datos SQLite.
3. Ejecuta el script de limpieza (`cleaning.py`).
4. Sube los archivos generados como artefactos.
5. Realiza un commit y push automático de los archivos generados al repositorio.

---

## **Requisitos Previos**
Antes de comenzar, asegúrate de tener instalado lo siguiente:
1. **Python 3.9 o superior**.
2. **pip** (gestor de paquetes de Python).
3. **Git** y **Git LFS** para clonar el repositorio y manejar archivos pesados.
4. **Cuenta en Kaggle** con credenciales configuradas para la API.

---

## **Instalación**

### **1. Clonar el repositorio**
Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/paezdev/Infra_Arqui_BigData2025Paez_Suarez.git
cd Infra_Arqui_BigData2025Paez_Suarez
```

### **2. Instalar Git LFS**
Si aún no tienes Git LFS instalado, configúralo en tu máquina local:
```bash
git lfs install
```

Asegúrate de que los archivos pesados se descarguen correctamente:
```bash
git lfs pull
```

### **3. Crear un entorno virtual**
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

### **4. Instalar las dependencias**
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

---

## **Automatización con GitHub Actions**
El proyecto incluye workflows de GitHub Actions para automatizar las etapas de ingesta y limpieza de datos. Los workflows se encuentran en la carpeta `.github/workflows`.

---

## **Autores**
- **Jean Carlos Páez Ramírez**
- **Juliana Maria Peña Suárez**

---

## **Licencia**
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.