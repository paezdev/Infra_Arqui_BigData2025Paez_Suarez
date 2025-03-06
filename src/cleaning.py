import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def connect_to_database():
    """
    Conecta con la base de datos SQLite generada en la Actividad 1.
    """
    print("Conectando a la base de datos...")
    db_path = 'src/static/db/ingestion.db'
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"No se encontró la base de datos en {db_path}")

    conn = sqlite3.connect(db_path)
    print("Conexión establecida correctamente.")
    return conn

def get_table_names(conn):
    """
    Obtiene los nombres de todas las tablas en la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    return tables

def exploratory_analysis(conn, tables):
    """
    Realiza un análisis exploratorio de los datos para identificar problemas de calidad.
    """
    print("Realizando análisis exploratorio...")
    analysis_results = {}

    for table in tables:
        print(f"Analizando tabla: {table}")
        df = pd.read_sql_query(f"SELECT * FROM '{table}'", conn)

        # Estadísticas básicas
        total_rows = len(df)
        null_values = df.isnull().sum().sum()
        duplicated_rows = df.duplicated().sum()

        # Tipos de datos
        data_types = df.dtypes.to_dict()

        # Almacenar resultados
        analysis_results[table] = {
            'total_rows': total_rows,
            'null_values': null_values,
            'duplicated_rows': duplicated_rows,
            'data_types': data_types,
            'dataframe': df  # Guardamos el DataFrame para procesamiento posterior
        }

        print(f"  - Filas totales: {total_rows}")
        print(f"  - Valores nulos: {null_values}")
        print(f"  - Filas duplicadas: {duplicated_rows}")

    return analysis_results

def clean_data(analysis_results):
    """
    Limpia y transforma los datos según los problemas identificados.
    """
    print("Iniciando proceso de limpieza de datos...")
    cleaned_results = {}
    cleaning_operations = {}

    for table, data in analysis_results.items():
        print(f"Limpiando tabla: {table}")
        df = data['dataframe'].copy()
        operations = []

        # 1. Eliminar duplicados
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        if duplicates_removed > 0:
            operations.append(f"Se eliminaron {duplicates_removed} filas duplicadas")

        # 2. Manejo de valores nulos
        null_counts_before = df.isnull().sum()

        # Para cada columna con valores nulos, aplicar una estrategia de imputación
        for column in df.columns:
            null_count = null_counts_before[column]
            if null_count > 0:
                # Estrategia según el tipo de dato
                if pd.api.types.is_numeric_dtype(df[column]):
                    # Para datos numéricos, usar la mediana
                    median_value = df[column].median()
                    df[column] = df[column].fillna(median_value)
                    operations.append(f"Se imputaron {null_count} valores nulos en '{column}' con la mediana ({median_value})")
                elif pd.api.types.is_datetime64_dtype(df[column]):
                    # Para fechas, usar la fecha más frecuente
                    mode_value = df[column].mode()[0]
                    df[column] = df[column].fillna(mode_value)
                    operations.append(f"Se imputaron {null_count} valores nulos en '{column}' con la moda")
                else:
                    # Para strings y otros tipos, usar 'DESCONOCIDO'
                    df[column] = df[column].fillna('DESCONOCIDO')
                    operations.append(f"Se imputaron {null_count} valores nulos en '{column}' con 'DESCONOCIDO'")

        # 3. Corrección de tipos de datos
        # Convertir columnas de fechas a datetime si tienen el formato adecuado
        date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        for col in date_columns:
            if not pd.api.types.is_datetime64_dtype(df[col]) and df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    operations.append(f"Se convirtió la columna '{col}' a tipo datetime")
                except:
                    operations.append(f"No se pudo convertir la columna '{col}' a tipo datetime")

        # 4. Transformaciones adicionales específicas según la tabla
        if table == 'olist_order_items_dataset':
            # Normalizar precios (por ejemplo, convertir a dólares si están en otra moneda)
            if 'price' in df.columns:
                df['price_normalized'] = df['price'] / 5.0  # Ejemplo: conversión a USD (asumiendo BRL)
                operations.append("Se normalizó la columna 'price' creando 'price_normalized'")

        elif table == 'olist_products_dataset':
            # Estandarizar nombres de categorías
            if 'product_category_name' in df.columns:
                df['product_category_name'] = df['product_category_name'].str.lower().str.replace('_', ' ')
                operations.append("Se estandarizaron los nombres de categorías de productos")

        elif table == 'olist_order_reviews_dataset':
            # Categorizar las puntuaciones de reseñas
            if 'review_score' in df.columns:
                bins = [0, 2, 3, 5]
                labels = ['Negativa', 'Neutral', 'Positiva']
                df['review_sentiment'] = pd.cut(df['review_score'], bins=bins, labels=labels)
                operations.append("Se categorizaron las puntuaciones de reseñas en sentimientos")

        # Guardar resultados
        cleaned_results[table] = df
        cleaning_operations[table] = operations

        print(f"  - Operaciones realizadas: {len(operations)}")

    return cleaned_results, cleaning_operations

def export_cleaned_data(cleaned_results):
    """
    Exporta los datos limpios a un archivo Excel o CSV.
    """
    print("Exportando datos limpios...")
    os.makedirs('src/static/csv', exist_ok=True)

    # Seleccionar una muestra representativa de cada tabla
    samples = []
    for table, df in cleaned_results.items():
        # Tomar una muestra proporcional al tamaño de la tabla
        sample_size = min(100, len(df))
        sample = df.sample(sample_size)
        sample['origen'] = table  # Añadir columna para identificar la tabla
        samples.append(sample)

    # Concatenar todas las muestras
    if samples:
        final_sample = pd.concat(samples)
        csv_path = 'src/static/xlsx/cleaned_data.csv'
        final_sample.to_csv(csv_path, index=False)
        print(f"Archivo csv con datos limpios generado en: {csv_path}")
    else:
        print("No se pudo generar el archivo de datos limpios.")

def generate_audit_report(analysis_results, cleaned_results, cleaning_operations):
    """
    Genera un archivo de auditoría que documenta las operaciones realizadas.
    """
    print("Generando reporte de auditoría...")
    os.makedirs('src/static/auditoria', exist_ok=True)

    audit_lines = [f"Reporte de Auditoría de Limpieza - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  "=" * 50]

    # Resumen general
    total_initial_records = sum(data['total_rows'] for data in analysis_results.values())
    total_final_records = sum(len(df) for df in cleaned_results.values())
    total_nulls_before = sum(data['null_values'] for data in analysis_results.values())
    total_nulls_after = sum(df.isnull().sum().sum() for df in cleaned_results.values())

    audit_lines.append(f"RESUMEN GENERAL:")
    audit_lines.append(f"- Registros antes de la limpieza: {total_initial_records}")
    audit_lines.append(f"- Registros después de la limpieza: {total_final_records}")
    audit_lines.append(f"- Valores nulos antes de la limpieza: {total_nulls_before}")
    audit_lines.append(f"- Valores nulos después de la limpieza: {total_nulls_after}")
    audit_lines.append(f"- Registros eliminados: {total_initial_records - total_final_records}")
    audit_lines.append(f"- Valores nulos tratados: {total_nulls_before - total_nulls_after}")
    audit_lines.append("")

    # Detalle por tabla
    audit_lines.append("DETALLE POR TABLA:")
    for table in analysis_results.keys():
        initial_data = analysis_results[table]
        final_data = cleaned_results[table]
        operations = cleaning_operations[table]

        audit_lines.append(f"\nTabla: {table}")
        audit_lines.append(f"- Registros antes: {initial_data['total_rows']}")
        audit_lines.append(f"- Registros después: {len(final_data)}")
        audit_lines.append(f"- Valores nulos antes: {initial_data['null_values']}")
        audit_lines.append(f"- Valores nulos después: {final_data.isnull().sum().sum()}")

        audit_lines.append("\nOperaciones realizadas:")
        for op in operations:
            audit_lines.append(f"  * {op}")

    # Escribir el reporte
    audit_text = "\n".join(audit_lines)
    audit_path = 'src/static/auditoria/cleaning_report.txt'
    with open(audit_path, 'w', encoding='utf-8') as f:
        f.write(audit_text)

    print(f"Archivo de auditoría generado en: {audit_path}")
    return audit_path

def save_cleaned_data_to_db(cleaned_results):
    """
    Guarda los datos limpios en una nueva base de datos SQLite.
    """
    print("Guardando datos limpios en base de datos...")
    os.makedirs('src/static/db', exist_ok=True)
    db_path = 'src/static/db/cleaned_data.db'

    # Eliminar la base de datos si ya existe
    if os.path.exists(db_path):
        print(f"Eliminando base de datos existente en {db_path}...")
        os.remove(db_path)

    # Crear nueva conexión
    conn = sqlite3.connect(db_path)

    # Guardar cada DataFrame limpio como una tabla
    for table_name, df in cleaned_results.items():
        clean_table_name = f"clean_{table_name}"
        print(f"Guardando tabla limpia: {clean_table_name}")
        df.to_sql(clean_table_name, conn, if_exists="replace", index=False)

    conn.close()
    print(f"Base de datos con datos limpios generada en: {db_path}")
    return db_path

def main():
    try:
        # Conectar a la base de datos
        conn = connect_to_database()

        # Obtener nombres de tablas
        tables = get_table_names(conn)

        # Análisis exploratorio
        analysis_results = exploratory_analysis(conn, tables)

        # Limpieza de datos
        cleaned_results, cleaning_operations = clean_data(analysis_results)

        # Exportar datos limpios a Excel
        export_cleaned_data(cleaned_results)

        # Guardar datos limpios en base de datos
        cleaned_db_path = save_cleaned_data_to_db(cleaned_results)

        # Generar reporte de auditoría
        audit_path = generate_audit_report(analysis_results, cleaned_results, cleaning_operations)

        # Actualizar el reporte de auditoría con información sobre la base de datos
        with open(audit_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\nDATOS LIMPIOS GUARDADOS EN BASE DE DATOS:")
            f.write(f"\n- Ruta: {cleaned_db_path}")
            f.write(f"\n- Tablas generadas: {', '.join([f'clean_{table}' for table in cleaned_results.keys()])}")

        # Cerrar conexión
        conn.close()

        print("Proceso de limpieza completado exitosamente.")

    except Exception as e:
        print(f"Error en el proceso de limpieza: {e}")
        raise

if __name__ == "__main__":
    main()