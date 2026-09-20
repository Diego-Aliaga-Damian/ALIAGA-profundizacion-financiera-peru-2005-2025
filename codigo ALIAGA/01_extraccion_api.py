# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 19/09/2026

import requests
from pathlib import Path
import csv
from datetime import datetime
FECHA_INICIO = "2005-1"
FECHA_CORTE = "2025-4"

# Códigos de las series del BCRPData
CODIGO_CREDITO_TOTAL = "PN03500MQ"
CODIGO_LIQUIDEZ = "PN03497MQ"
CODIGO_CREDITO_MN = "PN03498MQ"
CODIGO_CRECIMIENTO_PBI = "PN02507AQ"

# Unir los códigos de las cuatro series
SERIES = "-".join([
    CODIGO_CREDITO_TOTAL,
    CODIGO_LIQUIDEZ,
    CODIGO_CREDITO_MN,
    CODIGO_CRECIMIENTO_PBI
])

# Construir la URL de la API del BCRP
URL_API = (
    f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
    f"{SERIES}/json/{FECHA_INICIO}/{FECHA_CORTE}/esp"
)

print(URL_API)

# Realizar la solicitud a la API del BCRP con manejo de errores
try:
    respuesta = requests.get(URL_API, timeout=30)
    respuesta.raise_for_status()
    print("Código de estado:", respuesta.status_code)

except requests.exceptions.Timeout:
    print("Error: la API del BCRP tardó demasiado en responder.")
    raise

except requests.exceptions.ConnectionError:
    print("Error: no se pudo establecer conexión con la API del BCRP.")
    raise

except requests.exceptions.HTTPError as error:
    print("Error HTTP:", error)
    raise

except requests.exceptions.RequestException as error:
    print("Error durante la solicitud:", error)
    raise

# Convertir la respuesta de la API a formato JSON
datos = respuesta.json()

# Mostrar información básica recibida
print("Título:", datos["config"]["title"])
print("Número de periodos:", len(datos["periods"]))
print("Primer periodo:", datos["periods"][0]["name"])
print("Último periodo:", datos["periods"][-1]["name"])

# Verificar las series devueltas por la API
print("\nSeries recibidas:")

for i, serie in enumerate(datos["config"]["series"], start=1):
    print(i, serie["name"])

    # Definir la carpeta donde se guardarán los datos crudos
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos_crudos_ALIAGA"

# Crear la carpeta si no existiera
CARPETA_CRUDOS.mkdir(parents=True, exist_ok=True)

# Ruta del archivo JSON original
ARCHIVO_JSON = CARPETA_CRUDOS / "datos_crudos_e_2024200481m.json"

# Guardar exactamente la respuesta recibida del BCRP
ARCHIVO_JSON.write_bytes(respuesta.content)

print("\nDatos crudos guardados en:")
print(ARCHIVO_JSON)

# Ruta del archivo CSV de datos crudos
ARCHIVO_CSV = CARPETA_CRUDOS / "datos_crudos_e_2024200481m.csv"

# Guardar los datos recibidos en formato CSV
with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo)

    # Encabezados
    escritor.writerow([
        "periodo",
        "crecimiento_pbi",
        "liquidez_pbi",
        "credito_mn_pbi",
        "credito_total_pbi"
    ])

    # Escribir cada periodo con sus valores originales
    for periodo in datos["periods"]:
        escritor.writerow([
            periodo["name"],
            periodo["values"][0],
            periodo["values"][1],
            periodo["values"][2],
            periodo["values"][3]
        ])

print("\nCSV de datos crudos guardado en:")
print(ARCHIVO_CSV)

# Validar la cantidad de observaciones extraídas
numero_periodos = len(datos["periods"])

# Verificar si existen valores faltantes
valores_faltantes = 0

for periodo in datos["periods"]:
    for valor in periodo["values"]:
        if valor is None or valor == "":
            valores_faltantes += 1

print("\n--- VALIDACIÓN DE LA EXTRACCIÓN ---")
print("Número de observaciones:", numero_periodos)
print("Número de variables sustantivas:", len(datos["config"]["series"]))
print("Valores faltantes:", valores_faltantes)
print("Periodo inicial:", datos["periods"][0]["name"])
print("Periodo final:", datos["periods"][-1]["name"])

# Crear el registro de ejecución
ARCHIVO_LOG = CARPETA_PROYECTO / "log_ejecucion.txt"

with open(ARCHIVO_LOG, "w", encoding="utf-8") as log:
    log.write("REGISTRO DE EJECUCIÓN - FINANZAS I\n")
    log.write("=" * 50 + "\n")

    log.write(
        f"Fecha y hora: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    )

    log.write("Estudiante: Diego Sebastian Aliaga Damián\n")
    log.write("Matrícula: e_2024200481m\n")

    log.write(
        "Tema N.° 1: Profundización financiera y "
        "crecimiento económico en el Perú, 2005-2025\n"
    )

    log.write("Fuente: BCRPData\n")
    log.write(f"Estado HTTP: {respuesta.status_code}\n")

    log.write(
        f"Observaciones extraídas: {numero_periodos}\n"
    )

    log.write(
        f"Variables sustantivas: "
        f"{len(datos['config']['series'])}\n"
    )

    log.write(
        f"Valores faltantes: {valores_faltantes}\n"
    )

    log.write(
        f"Periodo inicial: {datos['periods'][0]['name']}\n"
    )

    log.write(
        f"Periodo final: {datos['periods'][-1]['name']}\n"
    )

    log.write(f"FECHA_INICIO: {FECHA_INICIO}\n")
    log.write(f"FECHA_CORTE: {FECHA_CORTE}\n")
    log.write(f"Endpoint: {URL_API}\n")

print("\nLog de ejecución guardado en:")
print(ARCHIVO_LOG)