# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 20/09/2026

import pandas as pd
from pathlib import Path
import hashlib

# ----------------------------------------------------------
# RUTAS DEL PROYECTO
# ----------------------------------------------------------

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent

CARPETA_CRUDOS = (
    CARPETA_PROYECTO / "datos_crudos_ALIAGA"
)

CARPETA_PROCESADOS = (
    CARPETA_PROYECTO / "datos_procesados_ALIAGA"
)

CARPETA_PROCESADOS.mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------------------------------
# ARCHIVOS DE ENTRADA
# ----------------------------------------------------------

ARCHIVO_BCRP = (
    CARPETA_CRUDOS /
    "datos_crudos_e_2024200481m.csv"
)

ARCHIVO_SBS = (
    CARPETA_CRUDOS /
    "datos_sbs_e_2024200481m.csv"
)

ARCHIVO_WDI = (
    CARPETA_CRUDOS /
    "datos_wdi_e_2024200481m.csv"
)

print("\n--- ARCHIVOS DE ENTRADA ---")
print("BCRP:", ARCHIVO_BCRP)
print("SBS:", ARCHIVO_SBS)
print("WDI:", ARCHIVO_WDI)

# ----------------------------------------------------------
# LECTURA DE DATOS CRUDOS
# ----------------------------------------------------------

df_bcrp = pd.read_csv(ARCHIVO_BCRP)
df_sbs = pd.read_csv(ARCHIVO_SBS)
df_wdi = pd.read_csv(ARCHIVO_WDI)

print("\n--- DIMENSIONES ORIGINALES ---")
print("BCRP:", df_bcrp.shape)
print("SBS:", df_sbs.shape)
print("WDI:", df_wdi.shape)

# ----------------------------------------------------------
# NORMALIZAR FECHAS DEL BCRP
# ----------------------------------------------------------

MESES_BCRP = {
    "Ene": 1,
    "Feb": 2,
    "Mar": 3,
    "Abr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dic": 12
}


def convertir_periodo_bcrp(periodo):
    mes_texto, anio = periodo.split(".")

    mes = MESES_BCRP[mes_texto]

    return f"{int(anio):04d}-{mes:02d}"


df_bcrp["fecha"] = (
    df_bcrp["periodo"]
    .apply(convertir_periodo_bcrp)
)

# Renombrar el PBI para identificar correctamente
# que corresponde a la serie desestacionalizada
df_bcrp = df_bcrp.rename(
    columns={
        "pbi_real": "pbi_desestacionalizado"
    }
)

print("\n--- FECHAS BCRP NORMALIZADAS ---")
print("Primera fecha:", df_bcrp["fecha"].iloc[0])
print("Última fecha:", df_bcrp["fecha"].iloc[-1])
print("Duplicados:", df_bcrp["fecha"].duplicated().sum())

# ----------------------------------------------------------
# VALIDAR FECHAS DE LA SBS
# ----------------------------------------------------------

df_sbs["fecha"] = df_sbs["fecha"].astype(str)

print("\n--- VALIDACIÓN SBS ---")
print("Primera fecha:", df_sbs["fecha"].iloc[0])
print("Última fecha:", df_sbs["fecha"].iloc[-1])
print("Duplicados:", df_sbs["fecha"].duplicated().sum())

# ----------------------------------------------------------
# UNIR DATOS MENSUALES BCRP Y SBS
# ----------------------------------------------------------

df_mensual = pd.merge(
    df_bcrp,
    df_sbs,
    on="fecha",
    how="inner",
    validate="one_to_one"
)

# Ordenar cronológicamente
df_mensual = df_mensual.sort_values(
    "fecha"
).reset_index(drop=True)

print("\n--- UNIÓN BCRP + SBS ---")
print("Número de observaciones:", len(df_mensual))
print("Número de columnas:", len(df_mensual.columns))
print("Primera fecha:", df_mensual["fecha"].iloc[0])
print("Última fecha:", df_mensual["fecha"].iloc[-1])
print(
    "Valores faltantes:",
    df_mensual.isna().sum().sum()
)
print(
    "Fechas duplicadas:",
    df_mensual["fecha"].duplicated().sum()
)

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

# ----------------------------------------------------------
# NORMALIZAR PERIODOS TRIMESTRALES DEL RATIO
# ----------------------------------------------------------

def convertir_periodo_trimestral(periodo):
    trimestre_texto, anio_corto = periodo.split(".")

    trimestre = int(trimestre_texto[1])
    anio = 2000 + int(anio_corto)

    return pd.Series({
        "anio": anio,
        "trimestre": trimestre,
        "periodo_trimestral": f"{anio}T{trimestre}"
    })


df_ratio[
    ["anio", "trimestre", "periodo_trimestral"]
] = df_ratio["periodo"].apply(
    convertir_periodo_trimestral
)

print("\n--- PERIODOS TRIMESTRALES NORMALIZADOS ---")
print(df_ratio.head())
print(df_ratio.tail())
print(
    "Duplicados:",
    df_ratio["periodo_trimestral"].duplicated().sum()
)

# ----------------------------------------------------------
# AGREGAR BASE MENSUAL A FRECUENCIA TRIMESTRAL
# ----------------------------------------------------------

df_mensual["fecha_dt"] = pd.to_datetime(
    df_mensual["fecha"] + "-01"
)

df_mensual["anio"] = df_mensual["fecha_dt"].dt.year

df_mensual["trimestre"] = (
    df_mensual["fecha_dt"].dt.quarter
)

df_mensual["periodo_trimestral"] = (
    df_mensual["anio"].astype(str)
    + "T"
    + df_mensual["trimestre"].astype(str)
)

df_trimestral = (
    df_mensual.groupby(
        ["anio", "trimestre", "periodo_trimestral"],
        as_index=False
    )
    .agg({
        "credito_sector_privado": "mean",
        "pbi_desestacionalizado": "mean",
        "inflacion_ipc": "mean",
        "tipo_cambio": "mean",
        "creditos_sbs_millones": "mean"
    })
)

print("\n--- BASE MENSUAL AGREGADA A TRIMESTRAL ---")
print("Número de observaciones:", len(df_trimestral))
print("Primera observación:")
print(df_trimestral.head(1))
print("Última observación:")
print(df_trimestral.tail(1))
print(
    "Valores faltantes:",
    df_trimestral.isna().sum().sum()
)

# ----------------------------------------------------------
# UNIR BASE TRIMESTRAL CON RATIO CRÉDITO / PBI
# ----------------------------------------------------------

df_final = pd.merge(
    df_trimestral,
    df_ratio[
        [
            "periodo_trimestral",
            "credito_privado_pct_pbi_bcrp"
        ]
    ],
    on="periodo_trimestral",
    how="inner",
    validate="one_to_one"
)

df_final = df_final.sort_values(
    ["anio", "trimestre"]
).reset_index(drop=True)

print("\n--- BASE TRIMESTRAL FINAL ---")
print("Número de observaciones:", len(df_final))
print("Número de columnas:", len(df_final.columns))
print(
    "Primer periodo:",
    df_final["periodo_trimestral"].iloc[0]
)
print(
    "Último periodo:",
    df_final["periodo_trimestral"].iloc[-1]
)
print(
    "Valores faltantes:",
    df_final.isna().sum().sum()
)
print(
    "Duplicados:",
    df_final["periodo_trimestral"].duplicated().sum()
)

print("\nColumnas finales:")
print(df_final.columns.tolist())

print("\nPrimeras observaciones:")
print(df_final.head())

# ----------------------------------------------------------
# GUARDAR BASES PROCESADAS
# ----------------------------------------------------------

ARCHIVO_MENSUAL_PROCESADO = (
    CARPETA_PROCESADOS /
    "datos_mensuales_procesados_e_2024200481m.csv"
)

ARCHIVO_TRIMESTRAL_PROCESADO = (
    CARPETA_PROCESADOS /
    "datos_procesados_e_2024200481m.csv"
)

# Guardar base mensual BCRP + SBS
df_mensual.to_csv(
    ARCHIVO_MENSUAL_PROCESADO,
    index=False,
    encoding="utf-8-sig"
)

# Guardar base trimestral principal
df_final.to_csv(
    ARCHIVO_TRIMESTRAL_PROCESADO,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- ARCHIVOS PROCESADOS GUARDADOS ---")
print("Base mensual:")
print(ARCHIVO_MENSUAL_PROCESADO)
print("Observaciones mensuales:", len(df_mensual))

print("\nBase trimestral:")
print(ARCHIVO_TRIMESTRAL_PROCESADO)
print("Observaciones trimestrales:", len(df_final))

# ----------------------------------------------------------
# GUARDAR WDI COMO SERIE COMPLEMENTARIA ANUAL
# ----------------------------------------------------------

ARCHIVO_WDI_PROCESADO = (
    CARPETA_PROCESADOS /
    "datos_wdi_procesados_e_2024200481m.csv"
)

df_wdi = df_wdi.sort_values(
    "anio"
).reset_index(drop=True)

df_wdi.to_csv(
    ARCHIVO_WDI_PROCESADO,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- WDI PROCESADO ---")
print("Observaciones:", len(df_wdi))
print("Primer año:", df_wdi["anio"].iloc[0])
print("Último año:", df_wdi["anio"].iloc[-1])
print("Valores faltantes:", df_wdi.isna().sum().sum())
print("Archivo:")
print(ARCHIVO_WDI_PROCESADO)

# ----------------------------------------------------------
# DICCIONARIO DE VARIABLES
# ----------------------------------------------------------

diccionario = pd.DataFrame([
    {
        "variable": "credito_sector_privado",
        "definicion": "Crédito total del sistema financiero al sector privado",
        "unidad": "Millones de soles",
        "frecuencia": "Trimestral (promedio de datos mensuales)",
        "fuente": "BCRPData",
        "codigo_serie": "PN00518MM",
        "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    },
    {
        "variable": "pbi_desestacionalizado",
        "definicion": "Producto Bruto Interno desestacionalizado",
        "unidad": "Índice 2007 = 100",
        "frecuencia": "Trimestral (promedio de datos mensuales)",
        "fuente": "BCRPData",
        "codigo_serie": "PN01773AM",
        "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    },
    {
        "variable": "inflacion_ipc",
        "definicion": "Variación porcentual del IPC de Lima Metropolitana en los últimos 12 meses",
        "unidad": "Porcentaje",
        "frecuencia": "Trimestral (promedio de datos mensuales)",
        "fuente": "BCRPData",
        "codigo_serie": "PN01273PM",
        "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    },
    {
        "variable": "tipo_cambio",
        "definicion": "Tipo de cambio interbancario promedio del periodo",
        "unidad": "Soles por US$",
        "frecuencia": "Trimestral (promedio de datos mensuales)",
        "fuente": "BCRPData",
        "codigo_serie": "PN01207PM",
        "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    },
    {
        "variable": "creditos_sbs_millones",
        "definicion": "Créditos directos de la banca múltiple",
        "unidad": "Millones de soles",
        "frecuencia": "Trimestral (promedio de datos mensuales)",
        "fuente": "SBS",
        "codigo_serie": "B-2332",
        "endpoint": "https://intranet2.sbs.gob.pe/estadistica/financiera/"
    },
    {
        "variable": "credito_privado_pct_pbi_bcrp",
        "definicion": "Crédito al sector privado como porcentaje del PBI",
        "unidad": "Porcentaje del PBI",
        "frecuencia": "Trimestral",
        "fuente": "BCRPData",
        "codigo_serie": "PN03500MQ",
        "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    },
    {
        "variable": "credito_privado_pct_pbi_wdi",
        "definicion": "Crédito interno al sector privado como porcentaje del PBI",
        "unidad": "Porcentaje del PBI",
        "frecuencia": "Anual",
        "fuente": "Banco Mundial - WDI",
        "codigo_serie": "FS.AST.PRVT.GD.ZS",
        "endpoint": "https://api.worldbank.org/v2/"
    }
])

ARCHIVO_DICCIONARIO = (
    CARPETA_PROCESADOS /
    "diccionario_variables_ALIAGA.csv"
)

diccionario.to_csv(
    ARCHIVO_DICCIONARIO,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- DICCIONARIO DE VARIABLES ---")
print("Variables documentadas:", len(diccionario))
print("Archivo:")
print(ARCHIVO_DICCIONARIO)

# ----------------------------------------------------------
# HASH SHA-256 DE LA BASE PROCESADA FINAL
# ----------------------------------------------------------

def calcular_sha256(ruta_archivo):
    sha256 = hashlib.sha256()

    with open(ruta_archivo, "rb") as archivo:
        for bloque in iter(lambda: archivo.read(8192), b""):
            sha256.update(bloque)

    return sha256.hexdigest()


HASH_BASE_FINAL = calcular_sha256(
    ARCHIVO_TRIMESTRAL_PROCESADO
)

ARCHIVO_HASH = (
    CARPETA_PROCESADOS /
    "hash_base_final_ALIAGA.txt"
)

with open(
    ARCHIVO_HASH,
    "w",
    encoding="utf-8"
) as archivo:
    archivo.write(
        f"Archivo: {ARCHIVO_TRIMESTRAL_PROCESADO.name}\n"
    )
    archivo.write(
        f"SHA-256: {HASH_BASE_FINAL}\n"
    )

print("\n--- HASH SHA-256 ---")
print("Archivo:", ARCHIVO_TRIMESTRAL_PROCESADO.name)
print("SHA-256:", HASH_BASE_FINAL)
print("Hash guardado en:")
print(ARCHIVO_HASH)