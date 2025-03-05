import os
import zipfile
import sqlite3
import pandas as pd
import kagglehub
from datetime import datetime

def download_dataset_zip():
    """
    Descarga el dataset desde Kaggle.
    Este método utiliza kagglehub.dataset_download, que descarga el dataset y devuelve la ruta donde se encuentra.
    """
    print("Descargando dataset desde Kaggle...")
    # Descarga el dataset; esto crea un directorio con los archivos descargados (puede incluir el .zip o los CSV)
    dataset_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    print("Ruta al dataset:", dataset_path)
    return dataset_path

def extract_zip_files(dataset_path):
    """
    Busca un archivo .zip en la ruta del dataset y, si lo encuentra, lo extrae en una carpeta 'extracted'
    dentro de esa ruta. Si no hay archivos .zip, verifica si ya existen archivos CSV, asumiendo que el dataset ya está extraído.
    """
    zip_files = [f for f in os.listdir(dataset_path) if f.endswith('.zip')]
    if zip_files:
        zip_file = os.path.join(dataset_path, zip_files[0])
        extract_dir = os.path.join(dataset_path, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        print(f"Extrayendo {zip_file} en {extract_dir}...")
        with zipfile.ZipFile(zip_file, "r") as z:
            z.extractall(extract_dir)
        return extract_dir
    else:
        # Si no se encuentra un ZIP, se verifica si existen archivos CSV en la ruta
        csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
        if csv_files:
            print("No se encontró archivo ZIP pero se detectaron archivos CSV; se asume que el dataset ya se encuentra extraído.")
            return dataset_path
        else:
            raise FileNotFoundError("No se encontró ningún archivo .zip ni archivos .csv en la ruta del dataset")

def create_database_from_csvs(csv_dir):
    """
    Recorre el directorio donde están los CSV y, para cada uno, crea una tabla en la base de datos SQLite.
    El nombre de la tabla se toma del nombre del archivo (sin extensión).
    """
    os.makedirs('src/static/db', exist_ok=True)
    db_path = 'src/static/db/ingestion.db'

    # Eliminar el archivo de base de datos si ya existe
    if os.path.exists(db_path):
        print(f"Eliminando base de datos existente en {db_path}...")
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("No se encontraron archivos CSV en el directorio extraído")

    for file in csv_files:
        file_path = os.path.join(csv_dir, file)
        print(f"Leyendo {file_path}...")
        try:
            df = pd.read_csv(file_path, encoding="latin1")
        except Exception as e:
            print(f"Error al leer {file}: {e}")
            continue
        table_name = os.path.splitext(file)[0]
        print(f"Creando/actualizando tabla '{table_name}' en la base de datos...")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print("Base de datos creada correctamente en:", db_path)

def generate_sample_file(csv_dir):
    """
    Para la evidencia complementaria, genera un archivo Excel que combine una muestra representativa de cada CSV.
    Se crea un DataFrame concatenando las primeras 10 filas de cada archivo y luego se exporta a Excel.
    """
    os.makedirs('src/static/xlsx', exist_ok=True)
    samples = []
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    for file in csv_files:
        file_path = os.path.join(csv_dir, file)
        try:
            df = pd.read_csv(file_path, encoding="latin1")
            sample = df.head(10)
            sample['origen'] = file  # Añadimos columna para identificar el origen de la muestra
            samples.append(sample)
        except Exception as e:
            print(f"Error al leer {file} para la muestra: {e}")
            continue
    if samples:
        final_sample = pd.concat(samples)
        excel_path = 'src/static/xlsx/ingestion.xlsx'
        final_sample.to_excel(excel_path, index=False)
        print("Archivo Excel de muestra generado en:", excel_path)
    else:
        print("No se generó archivo de muestra porque no se pudo leer ningún CSV.")

def generate_audit_file(dataset_path, csv_dir):
    """
    Genera un archivo de auditoría que compara el número total de registros extraídos de todos los CSV
    con la suma de registros insertados en las tablas de la base de datos.
    """
    audit_lines = []
    total_csv_records = 0
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    for file in csv_files:
        file_path = os.path.join(csv_dir, file)
        try:
            df = pd.read_csv(file_path, encoding="latin1")
            count = len(df)
            total_csv_records += count
            audit_lines.append(f"{file}: {count} registros")
        except Exception as e:
            audit_lines.append(f"{file}: error al leer ({e})")

    # Leer la base de datos y sumar registros de todas las tablas
    db_path = 'src/static/db/ingestion.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    total_db_records = 0
    for table in tables:
        tname = table[0]
        df_db = pd.read_sql_query(f"SELECT * FROM {tname}", conn)
        count_db = len(df_db)
        total_db_records += count_db
        audit_lines.append(f"Tabla '{tname}': {count_db} registros")
    conn.close()

    audit_text = f"""Reporte de Auditoría - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==============================
Total de registros en archivos CSV: {total_csv_records}
Total de registros en la base de datos: {total_db_records}

Detalle por archivo/tabla:
{chr(10).join(audit_lines)}
"""
    os.makedirs('src/static/auditoria', exist_ok=True)
    audit_path = 'src/static/auditoria/ingestion.txt'
    with open(audit_path, 'w', encoding='utf-8') as f:
        f.write(audit_text)
    print("Archivo de auditoría generado en:", audit_path)

def main():
    try:
        # Descarga y extracción
        dataset_path = download_dataset_zip()
        csv_dir = extract_zip_files(dataset_path)

        # Procesamiento: creación de base de datos, generación de muestra y auditoría
        create_database_from_csvs(csv_dir)
        generate_sample_file(csv_dir)
        generate_audit_file(dataset_path, csv_dir)

        print("Proceso completado exitosamente.")

    except Exception as e:
        print("Error en el proceso:", e)
        raise

if __name__ == "__main__":
    main()