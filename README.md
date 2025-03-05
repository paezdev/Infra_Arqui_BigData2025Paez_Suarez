# **BigData2025Act1Paez_Suarez&peña_juliana**

## **Descripción del Proyecto**
Este proyecto implementa la etapa de **ingesta de datos** del proyecto integrador de Big Data. El objetivo principal es extraer datos desde un API, almacenarlos en una base de datos SQLite y generar evidencias complementarias, como un archivo de muestra en formato Excel y un archivo de auditoría en formato `.txt`. Además, el proyecto está automatizado mediante **GitHub Actions**, lo que permite ejecutar el proceso de ingesta de datos de manera continua y dejar evidencia de los resultados.

### **Objetivos**
1. Leer datos desde un API (Kaggle).
2. Almacenar los datos en una base de datos SQLite.
3. Generar evidencias complementarias:
   - Un archivo Excel con una muestra representativa de los datos.
   - Un archivo de auditoría que compare los registros extraídos con los almacenados.
4. Automatizar el proceso mediante GitHub Actions.
5. Manejar archivos pesados (como la base de datos) utilizando **Git LFS**.

---

## **Estructura del Proyecto**
La estructura del proyecto es la siguiente:

```
BigData2025Act1Paez_Suarez/
├── setup.py                     # Configuración del proyecto y dependencias
├── README.md                    # Documentación del proyecto
├── .gitattributes               # Configuración de Git LFS para archivos pesados
├── .gitignore                   # Archivos y carpetas ignorados por Git
├── .github/
│   └── workflows/
│       └── bigdata.yml          # Workflow de GitHub Actions
├── src/
│   ├── ingestion.py             # Script principal de ingesta de datos
│   ├── static/
│       ├── auditoria/
│       │   └── ingestion.txt    # Archivo de auditoría generado
│       ├── db/
│       │   └── ingestion.db     # Base de datos SQLite generada (manejada con Git LFS)
│       └── xlsx/
│           └── ingestion.xlsx   # Archivo Excel de muestra generado
└── .venv/                       # Entorno virtual (ignorado por Git)
```

---

## **Gestión de Archivos Pesados con Git LFS**
Dado que la base de datos SQLite (`ingestion.db`) puede ser un archivo pesado, se configuró **Git LFS (Large File Storage)** para manejar este archivo de manera eficiente. Esto asegura que los archivos grandes no sobrecarguen el repositorio y se gestionen de forma adecuada.

### **Configuración de Git LFS**
1. **Instalación de Git LFS**:
   Si aún no tienes Git LFS instalado, puedes hacerlo con el siguiente comando:
   ```bash
   git lfs install
   ```

2. **Seguimiento de archivos pesados**:
   Se configuró el archivo `.gitattributes` para que Git LFS maneje el archivo `ingestion.db`:
   ```plaintext
   src/static/db/ingestion.db filter=lfs diff=lfs merge=lfs -text
   ```

3. **Agregar el archivo al seguimiento de Git LFS**:
   ```bash
   git lfs track "src/static/db/ingestion.db"
   ```

4. **Confirmar los cambios**:
   Asegúrate de que el archivo `.gitattributes` esté incluido en el repositorio:
   ```bash
   git add .gitattributes
   git commit -m "Configuración de Git LFS para archivos pesados"
   ```

5. **Subir los archivos al repositorio**:
   Una vez configurado, los archivos pesados serán manejados automáticamente por Git LFS al hacer `git push`.

---

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
git clone https://github.com/paez-dev/BigData2025Act1Paez_Suarez.git
cd BigData2025Act1Paez_Suarez
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
Crea un archivo `kaggle.json` con tus credenciales de Kaggle y colócalo en la carpeta `~/.kaggle` (en Windows, `C:\Users\<tu_usuario>\.kaggle`):

```json
{
  "username": "TU_USUARIO",
  "key": "TU_CLAVE_API"
}
```

Asegúrate de que el archivo tenga los permisos correctos:

```bash
chmod 600 ~/.kaggle/kaggle.json
```

### **2. Ejecutar el script de ingesta**
Ejecuta el script principal para realizar la ingesta de datos:

```bash
python src/ingestion.py
```

Este script realizará las siguientes tareas:
1. Descargar el dataset desde Kaggle.
2. Extraer los archivos CSV.
3. Crear una base de datos SQLite (`src/static/db/ingestion.db`) con los datos extraídos.
4. Generar un archivo Excel de muestra (`src/static/xlsx/ingestion.xlsx`).
5. Generar un archivo de auditoría (`src/static/auditoria/ingestion.txt`).

---

## **Automatización con GitHub Actions**

El proyecto incluye un workflow de GitHub Actions configurado en el archivo `.github/workflows/bigdata.yml`. Este workflow se ejecuta automáticamente en los siguientes casos:
- Cuando se realiza un `push` a la rama `main`.
- Cuando se crea un pull request hacia la rama `main`.
- Cuando se ejecuta manualmente desde la interfaz de GitHub.

### **Pasos del Workflow**
1. Configura Python 3.9 y las dependencias del proyecto.
2. Configura las credenciales de Kaggle.
3. Ejecuta el script de ingesta de datos.
4. Sube los archivos generados (`ingestion.db`, `ingestion.xlsx`, `ingestion.txt`) como artefactos.
5. Realiza un commit y push automático de los archivos generados al repositorio.

### **Verificación**
1. Ve a la pestaña **Actions** en el repositorio de GitHub.
2. Selecciona la ejecución más reciente del workflow.
3. Descarga los artefactos generados o verifica los archivos subidos al repositorio.

---

## **Archivos Generados**

### **1. Base de Datos SQLite**
- **Ruta:** `src/static/db/ingestion.db`
- Contiene las tablas generadas a partir de los archivos CSV descargados.
- **Nota:** Este archivo es manejado mediante **Git LFS** debido a su tamaño.

### **2. Archivo Excel de Muestra**
- **Ruta:** `src/static/xlsx/ingestion.xlsx`
- Contiene una muestra representativa (las primeras 10 filas) de cada archivo CSV.

### **3. Archivo de Auditoría**
- **Ruta:** `src/static/auditoria/ingestion.txt`
- Contiene un reporte que compara el número de registros extraídos de los archivos CSV con los registros almacenados en la base de datos.

---

## **Contribuciones**
Si deseas contribuir a este proyecto, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama para tus cambios:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz un commit:
   ```bash
   git commit -m "Descripción de los cambios"
   ```
4. Haz un push a tu rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un pull request en GitHub.

---

## **Autores**
- **Jean Carlos Páez Ramírez**
- **Juliana Maria Peña Suárez**

---

## **Licencia**
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
