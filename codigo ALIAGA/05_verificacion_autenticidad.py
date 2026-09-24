# Diego Sebastian Aliaga Damián
# Matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 20/09/2026

# ------------------------------------------------------------
# VERIFICACIÓN DE AUTENTICIDAD Y TRAZABILIDAD DE LOS DATOS
# ------------------------------------------------------------

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# RUTAS DEL PROYECTO
# ------------------------------------------------------------

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent

CARPETA_CRUDOS = (
    CARPETA_PROYECTO /
    "datos_crudos_ALIAGA"
)

CARPETA_PROCESADOS = (
    CARPETA_PROYECTO /
    "datos_procesados_ALIAGA"
)

CARPETA_SALIDAS = (
    CARPETA_PROYECTO /
    "salidas_ALIAGA"
)


# ------------------------------------------------------------
# ARCHIVOS UTILIZADOS
# ------------------------------------------------------------

ARCHIVO_BCRP = (
    CARPETA_CRUDOS /
    "datos_crudos_e_2024200481m.csv"
)

ARCHIVO_SBS = (
    CARPETA_CRUDOS /
    "datos_sbs_e_2024200481m.csv"
)

ARCHIVO_RATIO_BCRP = (
    CARPETA_CRUDOS /
    "ratio_credito_pbi_bcrp_e_2024200481m.csv"
)

ARCHIVO_FINAL = (
    CARPETA_PROCESADOS /
    "datos_procesados_e_2024200481m.csv"
)


print("\n--- VERIFICACIÓN DE AUTENTICIDAD ---")
print("Proyecto:", CARPETA_PROYECTO)
print("BCRP:", ARCHIVO_BCRP)
print("SBS:", ARCHIVO_SBS)
print("Ratio Crédito/PBI:", ARCHIVO_RATIO_BCRP)
print("Base final:", ARCHIVO_FINAL)

# ------------------------------------------------------------
# CARGA DE LOS DATOS
# ------------------------------------------------------------

df_bcrp = pd.read_csv(ARCHIVO_BCRP)
df_sbs = pd.read_csv(ARCHIVO_SBS)
df_ratio = pd.read_csv(ARCHIVO_RATIO_BCRP)
df_final = pd.read_csv(ARCHIVO_FINAL)


# ------------------------------------------------------------
# VERIFICACIÓN INICIAL
# ------------------------------------------------------------

print("\n--- DIMENSIONES DE LOS ARCHIVOS ---")
print("BCRP:", df_bcrp.shape)
print("SBS:", df_sbs.shape)
print("Ratio Crédito/PBI:", df_ratio.shape)
print("Base final:", df_final.shape)

print("\n--- COLUMNAS DISPONIBLES ---")
print("BCRP:", df_bcrp.columns.tolist())
print("SBS:", df_sbs.columns.tolist())
print("Ratio Crédito/PBI:", df_ratio.columns.tolist())
print("Base final:", df_final.columns.tolist())

print("\n--- VALORES FALTANTES ---")
print("BCRP:", df_bcrp.isna().sum().sum())
print("SBS:", df_sbs.isna().sum().sum())
print("Ratio Crédito/PBI:", df_ratio.isna().sum().sum())
print("Base final:", df_final.isna().sum().sum())

# ------------------------------------------------------------
# RECONSTRUCCIÓN TRIMESTRAL DESDE LOS DATOS CRUDOS
# ------------------------------------------------------------

# Normalizar fechas mensuales
# Convertir periodos BCRP en español: Ene.2005, Feb.2005, ...
MESES_BCRP = {
    "Ene": "01",
    "Feb": "02",
    "Mar": "03",
    "Abr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Ago": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dic": "12"
}

df_bcrp["mes_texto"] = (
    df_bcrp["periodo"]
    .str.split(".")
    .str[0]
)

df_bcrp["anio_texto"] = (
    df_bcrp["periodo"]
    .str.extract(r"(\d{4})")[0]
)

df_bcrp["fecha"] = pd.to_datetime(
    df_bcrp["anio_texto"]
    + "-"
    + df_bcrp["mes_texto"].map(MESES_BCRP),
    format="%Y-%m"
)

df_sbs["fecha"] = pd.to_datetime(
    df_sbs["fecha"],
    format="%Y-%m"
)

# Unir BCRP y SBS por mes
df_mensual = pd.merge(
    df_bcrp,
    df_sbs[["fecha", "creditos_sbs_millones"]],
    on="fecha",
    how="inner"
)

# Identificar año y trimestre
df_mensual["anio"] = df_mensual["fecha"].dt.year
df_mensual["trimestre"] = df_mensual["fecha"].dt.quarter

df_mensual["periodo_trimestral"] = (
    df_mensual["anio"].astype(str)
    + "T"
    + df_mensual["trimestre"].astype(str)
)

# Orden cronológico indispensable para usar "last"
df_mensual = (
    df_mensual
    .sort_values("fecha")
    .reset_index(drop=True)
)

# Aplicar exactamente las reglas de agregación de 03_limpieza_datos.py
df_reconstruida = (
    df_mensual
    .groupby(
        ["anio", "trimestre", "periodo_trimestral"],
        as_index=False
    )
    .agg({
        "credito_sector_privado": "last",
        "pbi_real": "mean",
        "inflacion_ipc": "mean",
        "tipo_cambio": "mean",
        "creditos_sbs_millones": "last"
    })
)

# Igualar el nombre utilizado en la base procesada
df_reconstruida = df_reconstruida.rename(
    columns={
        "pbi_real": "pbi_desestacionalizado"
    }
)

print("\n--- RECONSTRUCCIÓN DESDE DATOS CRUDOS ---")
print("Observaciones:", len(df_reconstruida))
print("Primer periodo:", df_reconstruida["periodo_trimestral"].iloc[0])
print("Último periodo:", df_reconstruida["periodo_trimestral"].iloc[-1])
print(
    "Valores faltantes:",
    df_reconstruida.isna().sum().sum()
)

# ------------------------------------------------------------
# COMPARACIÓN CON LA BASE PROCESADA FINAL
# ------------------------------------------------------------

variables_verificar = [
    "credito_sector_privado",
    "pbi_desestacionalizado",
    "inflacion_ipc",
    "tipo_cambio",
    "creditos_sbs_millones"
]

df_verificacion = pd.merge(
    df_final[
        ["periodo_trimestral"] + variables_verificar
    ],
    df_reconstruida[
        ["periodo_trimestral"] + variables_verificar
    ],
    on="periodo_trimestral",
    how="inner",
    suffixes=("_final", "_reconstruido")
)

print("\n--- COMPARACIÓN BASE FINAL VS. RECONSTRUCCIÓN ---")
print("Periodos comparados:", len(df_verificacion))

for variable in variables_verificar:

    diferencia = (
        df_verificacion[f"{variable}_final"]
        - df_verificacion[f"{variable}_reconstruido"]
    ).abs()

    discrepancias = (diferencia > 1e-8).sum()

    print(
        f"{variable}: "
        f"{discrepancias} discrepancias"
    )

print("\n--- FORMATOS DEL PERIODO DEL RATIO ---")
print("Base final:")
print(df_final["periodo_trimestral"].head(5).tolist())

print("Ratio crudo BCRP:")
print(df_ratio["periodo"].head(5).tolist())

# Normalizar periodo del ratio BCRP: T1.05 -> 2005T1
def normalizar_periodo_ratio(periodo):
    trimestre, anio_corto = periodo.split(".")
    anio = 2000 + int(anio_corto)
    return f"{anio}{trimestre}"


df_ratio["periodo_trimestral"] = (
    df_ratio["periodo"]
    .astype(str)
    .str.strip()
    .apply(normalizar_periodo_ratio)
)
# ------------------------------------------------------------
# VERIFICACIÓN DEL RATIO CRÉDITO / PBI DEL BCRP
# ------------------------------------------------------------

df_verificacion_ratio = pd.merge(
    df_final[
        [
            "periodo_trimestral",
            "credito_privado_pct_pbi_bcrp"
        ]
    ],
    df_ratio[
        [
            "periodo_trimestral",
            "credito_privado_pct_pbi_bcrp"
        ]
    ],
    on="periodo_trimestral",
    how="inner",
    suffixes=("_final", "_crudo")
)

diferencia_ratio = (
    df_verificacion_ratio["credito_privado_pct_pbi_bcrp_final"]
    - df_verificacion_ratio["credito_privado_pct_pbi_bcrp_crudo"]
).abs()

discrepancias_ratio = (diferencia_ratio > 1e-8).sum()

print("\n--- VERIFICACIÓN RATIO CRÉDITO / PBI BCRP ---")
print("Periodos comparados:", len(df_verificacion_ratio))
print("Discrepancias:", discrepancias_ratio)
print("Diferencia máxima:", diferencia_ratio.max())

# ------------------------------------------------------------
# SELECCIÓN DE 10 OBSERVACIONES PARA VERIFICACIÓN
# ------------------------------------------------------------

muestra_verificacion = (
    df_final
    .sample(n=10, random_state=2026)
    .sort_values(["anio", "trimestre"])
    .reset_index(drop=True)
)

print("\n--- MUESTRA DE 10 OBSERVACIONES PARA VERIFICACIÓN ---")
print(
    muestra_verificacion[
        [
            "periodo_trimestral",
            "credito_sector_privado",
            "pbi_desestacionalizado",
            "inflacion_ipc",
            "tipo_cambio",
            "creditos_sbs_millones",
            "credito_privado_pct_pbi_bcrp"
        ]
    ]
)

# ------------------------------------------------------------
# GUARDAR MUESTRA DE VERIFICACIÓN
# ------------------------------------------------------------

ARCHIVO_MUESTRA_VERIFICACION = (
    CARPETA_SALIDAS /
    "muestra_verificacion_autenticidad_ALIAGA.csv"
)

muestra_verificacion[
    [
        "periodo_trimestral",
        "credito_sector_privado",
        "pbi_desestacionalizado",
        "inflacion_ipc",
        "tipo_cambio",
        "creditos_sbs_millones",
        "credito_privado_pct_pbi_bcrp"
    ]
].to_csv(
    ARCHIVO_MUESTRA_VERIFICACION,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- MUESTRA DE VERIFICACIÓN GUARDADA ---")
print("Observaciones:", len(muestra_verificacion))
print("Archivo:")
print(ARCHIVO_MUESTRA_VERIFICACION)

# ------------------------------------------------------------
# VERIFICACIÓN DE LAS 10 OBSERVACIONES SELECCIONADAS
# ------------------------------------------------------------

columnas_verificar = [
    "credito_sector_privado",
    "pbi_desestacionalizado",
    "inflacion_ipc",
    "tipo_cambio",
    "creditos_sbs_millones"
]

# Comparar la muestra con la reconstrucción desde datos crudos
muestra_comprobada = pd.merge(
    muestra_verificacion[
        ["periodo_trimestral"] + columnas_verificar
    ],
    df_reconstruida[
        ["periodo_trimestral"] + columnas_verificar
    ],
    on="periodo_trimestral",
    how="left",
    suffixes=("_base", "_crudo")
)

# Incorporar el ratio Crédito/PBI directamente desde el archivo crudo BCRP
muestra_comprobada = pd.merge(
    muestra_comprobada,
    df_ratio[
        [
            "periodo_trimestral",
            "credito_privado_pct_pbi_bcrp"
        ]
    ],
    on="periodo_trimestral",
    how="left"
)

# Comparar las cinco variables reconstruidas
for variable in columnas_verificar:
    muestra_comprobada[f"verifica_{variable}"] = (
        (
            muestra_comprobada[f"{variable}_base"]
            - muestra_comprobada[f"{variable}_crudo"]
        ).abs()
        <= 1e-8
    )

# Comparar también el ratio Crédito/PBI
ratio_base = muestra_verificacion[
    [
        "periodo_trimestral",
        "credito_privado_pct_pbi_bcrp"
    ]
].rename(
    columns={
        "credito_privado_pct_pbi_bcrp":
        "credito_privado_pct_pbi_bcrp_base"
    }
)

muestra_comprobada = pd.merge(
    muestra_comprobada,
    ratio_base,
    on="periodo_trimestral",
    how="left"
)

muestra_comprobada["verifica_credito_pbi"] = (
    (
        muestra_comprobada["credito_privado_pct_pbi_bcrp_base"]
        - muestra_comprobada["credito_privado_pct_pbi_bcrp"]
    ).abs()
    <= 1e-8
)

# Resultado general por observación
columnas_verificacion = [
    f"verifica_{variable}"
    for variable in columnas_verificar
] + ["verifica_credito_pbi"]

muestra_comprobada["verificacion_total"] = (
    muestra_comprobada[columnas_verificacion]
    .all(axis=1)
)

print("\n--- VERIFICACIÓN DE LAS 10 OBSERVACIONES ---")
print(
    muestra_comprobada[
        [
            "periodo_trimestral",
            "verificacion_total"
        ]
    ]
)

print(
    "\nObservaciones verificadas:",
    int(muestra_comprobada["verificacion_total"].sum()),
    "de",
    len(muestra_comprobada)
)

# ------------------------------------------------------------
# GUARDAR EVIDENCIA DE VERIFICACIÓN
# ------------------------------------------------------------

ARCHIVO_EVIDENCIA_VERIFICACION = (
    CARPETA_SALIDAS /
    "evidencia_verificacion_autenticidad_ALIAGA.csv"
)

muestra_comprobada.to_csv(
    ARCHIVO_EVIDENCIA_VERIFICACION,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- EVIDENCIA DE AUTENTICIDAD GUARDADA ---")
print(
    "Observaciones verificadas:",
    int(muestra_comprobada["verificacion_total"].sum()),
    "de",
    len(muestra_comprobada)
)
print("Archivo:")
print(ARCHIVO_EVIDENCIA_VERIFICACION)