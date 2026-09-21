# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 20/09/2026

import requests
from pathlib import Path
import csv
from datetime import datetime
FECHA_INICIO = "2005-1"
FECHA_CORTE = "2025-12"

# Códigos de las series mensuales del BCRPData
CODIGO_CREDITO_TOTAL = "PN00518MM"
CODIGO_PBI_REAL = "PN01773AM"
CODIGO_INFLACION = "PN01273PM"
CODIGO_TIPO_CAMBIO = "PN01207PM"
# Unir los códigos de las series
SERIES = "-".join([
    CODIGO_CREDITO_TOTAL,
    CODIGO_PBI_REAL,
    CODIGO_INFLACION,
    CODIGO_TIPO_CAMBIO
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
    "credito_sector_privado",
    "tipo_cambio",
    "inflacion_ipc",
    "pbi_real"
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

# ----------------------------------------------------------
# BANCO MUNDIAL - WORLD DEVELOPMENT INDICATORS (WDI)
# ----------------------------------------------------------

INDICADOR_WDI = "FS.AST.PRVT.GD.ZS"
PAIS_WDI = "PER"

URL_WDI = (
    f"https://api.worldbank.org/v2/country/{PAIS_WDI}/"
    f"indicator/{INDICADOR_WDI}"
    f"?format=json&date=2005:2025&per_page=100"
)

# Descargar datos del Banco Mundial
respuesta_wdi = requests.get(
    URL_WDI,
    timeout=60
)

respuesta_wdi.raise_for_status()

datos_wdi = respuesta_wdi.json()

print("\n--- BANCO MUNDIAL WDI ---")
print("Código de estado:", respuesta_wdi.status_code)
print("Indicador:", INDICADOR_WDI)
print("País:", PAIS_WDI)

# Procesar observaciones del WDI
observaciones_wdi = datos_wdi[1]

registros_wdi = []

for observacion in observaciones_wdi:
    if observacion["value"] is not None:
        registros_wdi.append({
            "anio": int(observacion["date"]),
            "credito_privado_pct_pbi_wdi": observacion["value"]
        })

# Ordenar cronológicamente
registros_wdi = sorted(
    registros_wdi,
    key=lambda x: x["anio"]
)

print("Observaciones con datos:", len(registros_wdi))

if registros_wdi:
    print("Primer año:", registros_wdi[0]["anio"])
    print("Último año:", registros_wdi[-1]["anio"])
    print(
        "Último valor disponible:",
        registros_wdi[-1]["credito_privado_pct_pbi_wdi"]
    )

    # Guardar datos crudos del Banco Mundial
ARCHIVO_WDI = (
    Path("datos_crudos_ALIAGA")
    / "datos_wdi_e_2024200481m.csv"
)

with open(
    ARCHIVO_WDI,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:
    campos = [
        "anio",
        "credito_privado_pct_pbi_wdi"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=campos
    )

    escritor.writeheader()
    escritor.writerows(registros_wdi)

print("Datos WDI guardados en:")
print(ARCHIVO_WDI)

# ----------------------------------------------------------
# BCRP - RATIO CRÉDITO AL SECTOR PRIVADO / PBI
# SERIE OFICIAL TRIMESTRAL
# ----------------------------------------------------------

CODIGO_RATIO_CREDITO_PBI = "PN03500MQ"

URL_RATIO_BCRP = (
    "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
    f"{CODIGO_RATIO_CREDITO_PBI}/json/2005-1/2025-4/esp"
)

respuesta_ratio = requests.get(
    URL_RATIO_BCRP,
    timeout=60
)

respuesta_ratio.raise_for_status()

datos_ratio = respuesta_ratio.json()

print("\n--- BCRP RATIO CRÉDITO / PBI ---")
print("Código de estado:", respuesta_ratio.status_code)
print("Serie:", CODIGO_RATIO_CREDITO_PBI)
print("Título:", datos_ratio["config"]["title"])
print("Número de periodos:", len(datos_ratio["periods"]))
print("Primer periodo:", datos_ratio["periods"][0]["name"])
print("Último periodo:", datos_ratio["periods"][-1]["name"])

# ----------------------------------------------------------
# GUARDAR RATIO CRÉDITO / PBI DEL BCRP
# ----------------------------------------------------------

registros_ratio = []

for periodo in datos_ratio["periods"]:
    valor = periodo["values"][0]

    if valor is not None:
        registros_ratio.append({
            "periodo": periodo["name"],
            "credito_privado_pct_pbi_bcrp": float(valor)
        })

ARCHIVO_RATIO_BCRP = (
    Path("datos_crudos_ALIAGA")
    / "ratio_credito_pbi_bcrp_e_2024200481m.csv"
)

with open(
    ARCHIVO_RATIO_BCRP,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:

    campos = [
        "periodo",
        "credito_privado_pct_pbi_bcrp"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=campos
    )

    escritor.writeheader()
    escritor.writerows(registros_ratio)

print("\n--- GUARDADO RATIO CRÉDITO / PBI ---")
print("Observaciones guardadas:", len(registros_ratio))
print("Archivo guardado en:")
print(ARCHIVO_RATIO_BCRP)

# ----------------------------------------------------------
# LEER RATIO OFICIAL CRÉDITO / PBI DEL BCRP
# ----------------------------------------------------------

ARCHIVO_RATIO_BCRP = (
    CARPETA_CRUDOS /
    "ratio_credito_pbi_bcrp_e_2024200481m.csv"
)

df_ratio = pd.read_csv(
    ARCHIVO_RATIO_BCRP
)

print("\n--- RATIO CRÉDITO / PBI BCRP ---")
print("Número de observaciones:", len(df_ratio))
print("Columnas:", df_ratio.columns.tolist())
print("Primeras observaciones:")
print(df_ratio.head())
print("Últimas observaciones:")
print(df_ratio.tail())
print(
    "Valores faltantes:",
    df_ratio.isna().sum().sum()
)