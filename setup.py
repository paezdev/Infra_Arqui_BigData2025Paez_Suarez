from setuptools import setup, find_packages

setup(
    name="ingestion-bigdata",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "kagglehub[pandas-datasets]>=0.3.8",
        "openpyxl>=3.1.2",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.2",
        "numpy>=1.20.0"
    ],
    author="Jean Carlos Páez Ramírez y Juliana Maria Peña Suarez",
    author_email="",
    asignatura="Infraestructura y arquitectura para Big Data",
    tema="Ingestión y procesamiento de Datos",    
    description="Etapas de ingesta y preprocesamiento de datos para el proyecto integrador de infraestructura y arquitectura para Big Data",
    docente="Andres Felipe Callejas Jaramillo",
    python_requires=">=3.9",
)