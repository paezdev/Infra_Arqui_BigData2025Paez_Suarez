import pandas as pd
import sqlite3
import os
from datetime import datetime
import json
import xml.etree.ElementTree as ET

def load_cleaned_data():
    """
    Carga los datos limpios desde la base de datos SQLite.
    """
    print("Cargando datos limpios...")
    db_path = 'src/static/db/cleaned_data.db'
    conn = sqlite3.connect(db_path)

    # Obtener todas las tablas
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    dataframes = {}

    for table in tables['name']:
        dataframes[table] = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        print(f"Tabla {table} cargada: {len(dataframes[table])} registros")

    conn.close()
    return dataframes

def create_additional_data():
    """
    Crea archivos de datos adicionales en diferentes formatos.
    """
    print("Creando archivos de datos adicionales...")

    # Crear directorios si no existen
    os.makedirs('src/static/json', exist_ok=True)
    os.makedirs('src/static/xlsx', exist_ok=True)
    os.makedirs('src/static/csv', exist_ok=True)
    os.makedirs('src/static/xml', exist_ok=True)
    os.makedirs('src/static/html', exist_ok=True)
    os.makedirs('src/static/txt', exist_ok=True)

    # 1. Crear datos adicionales en JSON
    product_categories = {
        "additional_categories": [
            {"category_id": "CAT001", "category_name": "Electronics", "tax_rate": 0.19},
            {"category_id": "CAT002", "category_name": "Home & Garden", "tax_rate": 0.16},
            {"category_id": "CAT003", "category_name": "Fashion", "tax_rate": 0.12}
        ]
    }

    with open('src/static/json/additional_data.json', 'w') as f:
        json.dump(product_categories, f, indent=4)

    # 2. Crear datos adicionales en XLSX
    shipping_rates = pd.DataFrame({
        'weight_range': ['0-1kg', '1-2kg', '2-5kg', '5-10kg', '>10kg'],
        'base_rate': [10.0, 15.0, 25.0, 40.0, 60.0],
        'express_rate': [20.0, 30.0, 45.0, 70.0, 100.0]
    })
    shipping_rates.to_excel('src/static/xlsx/additional_data.xlsx', index=False)

    # 3. Crear datos adicionales en CSV
    customer_segments = pd.DataFrame({
        'segment_id': ['S1', 'S2', 'S3', 'S4'],
        'segment_name': ['Bronze', 'Silver', 'Gold', 'Platinum'],
        'min_purchase': [0, 1000, 5000, 10000],
        'discount_rate': [0.00, 0.05, 0.10, 0.15]
    })
    customer_segments.to_csv('src/static/csv/additional_data.csv', index=False)

    # 4. Crear datos adicionales en XML
    root = ET.Element("payment_methods")
    methods = [
        {"id": "PM001", "name": "Credit Card", "processing_fee": "2.5"},
        {"id": "PM002", "name": "Debit Card", "processing_fee": "1.5"},
        {"id": "PM003", "name": "Bank Transfer", "processing_fee": "0.5"}
    ]

    for method in methods:
        elem = ET.SubElement(root, "payment_method")
        for key, value in method.items():
            ET.SubElement(elem, key).text = value

    tree = ET.ElementTree(root)
    tree.write('src/static/xml/additional_data.xml')

    # 5. Crear datos adicionales en HTML
    html_content = """
    <table>
        <tr><th>Delivery Service</th><th>Delivery Time</th><th>Cost Factor</th></tr>
        <tr><td>Standard</td><td>3-5 days</td><td>1.0</td></tr>
        <tr><td>Express</td><td>1-2 days</td><td>1.5</td></tr>
        <tr><td>Same Day</td><td>24 hours</td><td>2.0</td></tr>
    </table>
    """

    with open('src/static/html/additional_data.html', 'w') as f:
        f.write(html_content)

    # 6. Crear datos adicionales en TXT
    txt_content = """
    Supplier Ratings:
    A - Premium Supplier (Discount: 15%)
    B - Standard Supplier (Discount: 10%)
    C - Basic Supplier (Discount: 5%)
    """

    with open('src/static/txt/additional_data.txt', 'w') as f:
        f.write(txt_content)

def read_additional_sources():
    """
    Lee las fuentes adicionales en diferentes formatos.
    """
    print("Leyendo fuentes adicionales...")
    additional_data = {}

    # 1. Leer JSON
    with open('src/static/json/additional_data.json', 'r') as f:
        additional_data['json_data'] = pd.DataFrame(json.load(f)['additional_categories'])

    # 2. Leer XLSX
    additional_data['xlsx_data'] = pd.read_excel('src/static/xlsx/additional_data.xlsx')

    # 3. Leer CSV
    additional_data['csv_data'] = pd.read_csv('src/static/csv/additional_data.csv')

    # 4. Leer XML
    tree = ET.parse('src/static/xml/additional_data.xml')
    root = tree.getroot()
    xml_data = []
    for method in root.findall('payment_method'):
        xml_data.append({
            'id': method.find('id').text,
            'name': method.find('name').text,
            'processing_fee': float(method.find('processing_fee').text)
        })
    additional_data['xml_data'] = pd.DataFrame(xml_data)

    # 5. Leer HTML
    additional_data['html_data'] = pd.read_html('src/static/html/additional_data.html')[0]

    # 6. Leer TXT
    with open('src/static/txt/additional_data.txt', 'r') as f:
        additional_data['txt_data'] = f.read()

    return additional_data

def enrich_data(cleaned_data, additional_data):
    """
    Integra los datos limpios con las fuentes adicionales.
    """
    print("Enriqueciendo datos...")
    enriched_data = {}

    # 1. Enriquecer productos con categorías adicionales
    products_df = cleaned_data['clean_olist_products_dataset'].copy()
    categories_df = additional_data['json_data']
    enriched_data['products'] = products_df.merge(
        categories_df,
        left_on='product_category_name',
        right_on='category_name',
        how='left'
    )

    # 2. Enriquecer órdenes con información de envío
    orders_df = cleaned_data['clean_olist_orders_dataset'].copy()
    shipping_df = additional_data['xlsx_data']
    # Aquí agregarías la lógica para determinar el weight_range
    orders_df['weight_range'] = '0-1kg'  # Ejemplo simplificado
    enriched_data['orders'] = orders_df.merge(
        shipping_df,
        on='weight_range',
        how='left'
    )

    # 3. Enriquecer clientes con segmentos
    customers_df = cleaned_data['clean_olist_customers_dataset'].copy()
    segments_df = additional_data['csv_data']
    # Aquí agregarías la lógica para calcular min_purchase
    customers_df['min_purchase'] = 0  # Ejemplo simplificado
    enriched_data['customers'] = customers_df.merge(
        segments_df,
        on='min_purchase',
        how='left'
    )

    return enriched_data

def save_results(enriched_data):
    """
    Guarda los resultados del enriquecimiento.
    """
    print("Guardando resultados...")

    # 1. Guardar datos enriquecidos en Excel
    os.makedirs('src/static/xlsx', exist_ok=True)
    writer = pd.ExcelWriter('src/static/xlsx/enriched_data.xlsx', engine='openpyxl')

    for name, df in enriched_data.items():
        df.to_excel(writer, sheet_name=name, index=False)

    writer.close()

    # 2. Crear reporte de auditoría
    os.makedirs('src/static/auditoria', exist_ok=True)
    audit_content = f"""Reporte de Enriquecimiento de Datos - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===============================

1. Resumen de Datos Enriquecidos:
"""

    for name, df in enriched_data.items():
        audit_content += f"\n{name.upper()}:"
        audit_content += f"\n- Registros: {len(df)}"
        audit_content += f"\n- Columnas: {', '.join(df.columns)}"
        audit_content += "\n"

    with open('src/static/auditoria/enriched_report.txt', 'w') as f:
        f.write(audit_content)

def save_final_db(cleaned_data, enriched_data):
    """
    Guarda en una única base de datos las tablas con los nombres finales deseados,
    combinando datos limpios y enriquecidos, y genera el archivo "enriched_data.db".
    """
    print("Generando la base de datos final con tablas limpias y enriquecidas...")

    # Ruta donde se creará la base de datos final
    os.makedirs('src/static/db', exist_ok=True)
    db_path = 'src/static/db/enriched_data.db'

    # Eliminar la base de datos si ya existe
    if os.path.exists(db_path):
        print(f"Eliminando base de datos existente en {db_path}...")
        os.remove(db_path)

    # Crear conexión a la base de datos
    conn = sqlite3.connect(db_path)

    # Mapeo de nombre de tabla final -> DataFrame de origen
    # En este mapeo se indica qué tablas se guardan enriquecidas y cuáles se mantienen limpias
    final_tables = {
        # Tablas enriquecidas
        "enriched_olist_customers_dataset": enriched_data["customers"],
        "enriched_olist_orders_dataset": enriched_data["orders"],
        "enriched_olist_products_dataset": enriched_data["products"],

        # Tablas limpias (ya reprocesadas en otro .py)
        "clean_olist_geolocation_dataset": cleaned_data["clean_olist_geolocation_dataset"],
        "clean_olist_order_items_dataset": cleaned_data["clean_olist_order_items_dataset"],
        "clean_olist_order_payments_dataset": cleaned_data["clean_olist_order_payments_dataset"],
        "clean_olist_order_reviews_dataset": cleaned_data["clean_olist_order_reviews_dataset"],
        "clean_olist_sellers_dataset": cleaned_data["clean_olist_sellers_dataset"],
        "clean_product_category_name_translation": cleaned_data["clean_product_category_name_translation"]
    }

    # Guardar cada tabla en la base de datos con su nombre final
    for final_name, df in final_tables.items():
        print(f"Guardando tabla '{final_name}' con {len(df)} registros.")
        df.to_sql(final_name, conn, if_exists="replace", index=False)

    conn.close()
    print(f"Base de datos final generada en: {db_path}")
    return db_path


def main():
    """
    Función principal que ejecuta el proceso de enriquecimiento.
    """
    try:
        # 1. Cargar datos limpios
        cleaned_data = load_cleaned_data()

        # 2. Crear archivos de datos adicionales
        create_additional_data()

        # 3. Leer fuentes adicionales
        additional_data = read_additional_sources()

        # 4. Enriquecer datos
        enriched_data = enrich_data(cleaned_data, additional_data)

        # 5. Guardar resultados
        save_results(enriched_data)

        # 6. Guardar la base de datos final (archivo: enriched_data.db)
        save_final_db(cleaned_data, enriched_data)

        print("Proceso de enriquecimiento completado exitosamente.")

    except Exception as e:
        print(f"Error en el proceso de enriquecimiento: {e}")
        raise

if __name__ == "__main__":
    main()