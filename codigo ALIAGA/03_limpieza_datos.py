# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 19/09/2026

import csv
from pathlib import Path
import hashlib
# Definir las rutas del proyecto
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos_crudos_ALIAGA"
CARPETA_PROCESADOS = CARPETA_PROYECTO / "datos_procesados_ALIAGA"

# Definir el archivo de entrada
ARCHIVO_CRUDO = CARPETA_CRUDOS / "datos_crudos_e_2024200481m.csv"

print("Archivo crudo encontrado en:")
print(ARCHIVO_CRUDO)

# Endpoint utilizado para obtener los datos originales del BCRP
URL_API = (
    "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
    "PN03500MQ-PN03497MQ-PN03498MQ-PN02507AQ/"
    "json/2005-1/2025-4/esp"
)
# Leer los datos crudos
with open(ARCHIVO_CRUDO, "r", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    datos_crudos = list(lector)

# Verificar la lectura de los datos
print("\n--- LECTURA DE DATOS CRUDOS ---")
print("Número de filas:", len(datos_crudos))
print("Columnas:", lector.fieldnames)

# Transformar el periodo y construir los datos procesados
datos_procesados = []

for fila in datos_crudos:
    periodo_original = fila["periodo"]

    # Separar trimestre y año del formato original del BCRP
    trimestre = int(periodo_original[1])
    anio_corto = int(periodo_original.split(".")[1])

    # Convertir el año de dos dígitos a cuatro dígitos
    anio = 2000 + anio_corto

    # Crear el nuevo formato del periodo
    periodo_nuevo = f"{anio}T{trimestre}"

    # Construir la fila procesada
    nueva_fila = {
        "periodo": periodo_nuevo,
        "año": anio,
        "trimestre": trimestre,
        "crecimiento_pbi": float(fila["crecimiento_pbi"]),
        "liquidez_pbi": float(fila["liquidez_pbi"]),
        "credito_mn_pbi": float(fila["credito_mn_pbi"]),
        "credito_total_pbi": float(fila["credito_total_pbi"])
    }

    datos_procesados.append(nueva_fila)

# Mostrar las primeras observaciones transformadas
print("\n--- PRIMERAS FILAS PROCESADAS ---")

for fila in datos_procesados[:5]:
    print(fila)

    # Validar los datos procesados
print("\n--- VALIDACIÓN DE DATOS PROCESADOS ---")
print("Número de filas:", len(datos_procesados))
print("Número de columnas:", len(datos_procesados[0]))
print("Periodo inicial:", datos_procesados[0]["periodo"])
print("Periodo final:", datos_procesados[-1]["periodo"])

# Verificar que no existan periodos duplicados
periodos = [fila["periodo"] for fila in datos_procesados]
duplicados = len(periodos) - len(set(periodos))

print("Periodos duplicados:", duplicados)

# Definir la ruta del archivo procesado
ARCHIVO_PROCESADO = CARPETA_PROCESADOS / "datos_procesados_e_2024200481m.csv"

# Crear la carpeta de datos procesados si no existiera
CARPETA_PROCESADOS.mkdir(parents=True, exist_ok=True)

# Definir las columnas del archivo procesado
columnas = [
    "periodo",
    "año",
    "trimestre",
    "crecimiento_pbi",
    "liquidez_pbi",
    "credito_mn_pbi",
    "credito_total_pbi"
]

# Guardar los datos procesados
with open(ARCHIVO_PROCESADO, "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(datos_procesados)

print("\nDatos procesados guardados en:")
print(ARCHIVO_PROCESADO)

# Crear el diccionario de variables
DICCIONARIO = [
    {
        "variable": "periodo",
        "definicion": "Periodo trimestral de la observación",
        "unidad": "Año-trimestre",
        "frecuencia": "Trimestral",
        "fuente": "Variable derivada a partir del periodo reportado por BCRPData",
        "codigo_serie": "No aplica",
        "endpoint": URL_API
    },
    {
        "variable": "año",
        "definicion": "Año correspondiente a la observación",
        "unidad": "Año",
        "frecuencia": "Trimestral",
        "fuente": "Variable derivada a partir del periodo reportado por BCRPData",
        "codigo_serie": "No aplica",
        "endpoint": URL_API
    },
    {
        "variable": "trimestre",
        "definicion": "Trimestre correspondiente a la observación",
        "unidad": "Trimestre",
        "frecuencia": "Trimestral",
        "fuente": "Variable derivada a partir del periodo reportado por BCRPData",
        "codigo_serie": "No aplica",
        "endpoint": URL_API
    },
    {
        "variable": "crecimiento_pbi",
        "definicion": "Producto bruto interno - PBI Global, variación porcentual interanual",
        "unidad": "Porcentaje",
        "frecuencia": "Trimestral",
        "fuente": "BCRPData - Banco Central de Reserva del Perú",
        "codigo_serie": "PN02507AQ",
        "endpoint": URL_API
    },
    {
        "variable": "liquidez_pbi",
        "definicion": "Liquidez total como porcentaje del PBI",
        "unidad": "Porcentaje del PBI",
        "frecuencia": "Trimestral",
        "fuente": "BCRPData - Banco Central de Reserva del Perú",
        "codigo_serie": "PN03497MQ",
        "endpoint": URL_API
    },
    {
        "variable": "credito_mn_pbi",
        "definicion": "Crédito al sector privado en moneda nacional como porcentaje del PBI",
        "unidad": "Porcentaje del PBI",
        "frecuencia": "Trimestral",
        "fuente": "BCRPData - Banco Central de Reserva del Perú",
        "codigo_serie": "PN03498MQ",
        "endpoint": URL_API
    },
    {
        "variable": "credito_total_pbi",
        "definicion": "Crédito total al sector privado como porcentaje del PBI",
        "unidad": "Porcentaje del PBI",
        "frecuencia": "Trimestral",
        "fuente": "BCRPData - Banco Central de Reserva del Perú",
        "codigo_serie": "PN03500MQ",
        "endpoint": URL_API
    }
]

# Ruta del diccionario de variables
ARCHIVO_DICCIONARIO = (
    CARPETA_PROCESADOS / "diccionario_variables_ALIAGA.csv"
)

# Columnas del diccionario
columnas_diccionario = [
    "variable",
    "definicion",
    "unidad",
    "frecuencia",
    "fuente",
    "codigo_serie",
    "endpoint"
]

# Guardar el diccionario de variables
with open(
    ARCHIVO_DICCIONARIO,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:
    escritor = csv.DictWriter(
        archivo,
        fieldnames=columnas_diccionario
    )
    escritor.writeheader()
    escritor.writerows(DICCIONARIO)

print("\nDiccionario de variables guardado en:")
print(ARCHIVO_DICCIONARIO)

# ============================================================
# CALCULAR HASH SHA-256 DEL ARCHIVO PROCESADO
# ============================================================

def calcular_sha256(ruta_archivo):
    sha256 = hashlib.sha256()

    with open(ruta_archivo, "rb") as archivo:
        for bloque in iter(lambda: archivo.read(8192), b""):
            sha256.update(bloque)

    return sha256.hexdigest()


hash_procesado = calcular_sha256(ARCHIVO_PROCESADO)

print("\n--- HASH SHA-256 ---")
print("Archivo:", ARCHIVO_PROCESADO.name)
print("SHA-256:", hash_procesado)