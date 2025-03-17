import pandas as pd
import sqlite3
import os

def load_cleaned_data():
    """
    Carga los datos limpios desde la base de datos SQLite.
    """
    db_path = 'src/static/db/cleaned_data.db'
    conn = sqlite3.connect(db_path)
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    dataframes = {}
    for table in tables['name']:
        dataframes[table] = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return dataframes

def read_additional_sources():
    """
    Lee fuentes adicionales en formatos JSON, XLSX, CSV, XML, HTML y TXT.
    """
    additional_data = {}
    additional_data['json_data'] = pd.read_json('src/static/json/additional_data.json')
    additional_data['xlsx_data'] = pd.read_excel('src/static/xlsx/additional_data.xlsx')
    additional_data['csv_data'] = pd.read_csv('src/static/csv/additional_data.csv')
    # Puedes agregar más formatos aquí si es necesario
    return additional_data

def integrate_data(cleaned_data, additional_data):
    """
    Integra los datos limpios con las fuentes adicionales.
    """
    # Ejemplo de integración: unir datos por una clave común
    enriched_data = cleaned_data['clean_olist_orders_dataset'].merge(
        additional_data['csv_data'], on='order_id', how='left'
    )
    return enriched_data

def save_results(enriched_data):
    """
    Guarda los resultados del enriquecimiento en archivos.
    """
    os.makedirs('src/static/xlsx', exist_ok=True)
    os.makedirs('src/static/auditoria', exist_ok=True)

    # Guardar dataset enriquecido
    enriched_data.to_excel('src/static/xlsx/enriched_data.xlsx', index=False)

    # Crear reporte de auditoría
    with open('src/static/auditoria/enriched_report.txt', 'w') as f:
        f.write("Reporte de Enriquecimiento\n")
        f.write(f"Registros en el dataset enriquecido: {len(enriched_data)}\n")

def main():
    """
    Función principal para ejecutar el proceso de enriquecimiento.
    """
    print("Cargando datos limpios...")
    cleaned_data = load_cleaned_data()

    print("Leyendo fuentes adicionales...")
    additional_data = read_additional_sources()

    print("Integrando datos...")
    enriched_data = integrate_data(cleaned_data, additional_data)

    print("Guardando resultados...")
    save_results(enriched_data)

    print("Proceso de enriquecimiento completado.")

if __name__ == "__main__":
    main()