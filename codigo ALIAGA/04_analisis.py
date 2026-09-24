# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 20/09/2026

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ----------------------------------------------------------
# RUTAS DEL PROYECTO
# ----------------------------------------------------------

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_PROCESADOS = CARPETA_PROYECTO / "datos_procesados_ALIAGA"
CARPETA_SALIDAS = CARPETA_PROYECTO / "salidas_ALIAGA"

CARPETA_SALIDAS.mkdir(
    parents=True,
    exist_ok=True
)

ARCHIVO_DATOS = (
    CARPETA_PROCESADOS /
    "datos_procesados_e_2024200481m.csv"
)

print("Base de datos para el análisis:")
print(ARCHIVO_DATOS)

# ----------------------------------------------------------
# LEER BASE TRIMESTRAL PROCESADA
# ----------------------------------------------------------

df = pd.read_csv(
    ARCHIVO_DATOS
)

print("\n--- VERIFICACIÓN DE LA BASE ---")
print("Número de observaciones:", len(df))
print("Número de columnas:", len(df.columns))
print("Columnas:")
print(df.columns.tolist())

print(
    "Primer periodo:",
    df["periodo_trimestral"].iloc[0]
)

print(
    "Último periodo:",
    df["periodo_trimestral"].iloc[-1]
)

print(
    "Valores faltantes:",
    df.isna().sum().sum()
)

print(
    "Periodos duplicados:",
    df["periodo_trimestral"].duplicated().sum()
)

# ----------------------------------------------------------
# ESTADÍSTICAS DESCRIPTIVAS
# ----------------------------------------------------------

VARIABLES_ANALISIS = [
    "credito_sector_privado",
    "pbi_desestacionalizado",
    "inflacion_ipc",
    "tipo_cambio",
    "creditos_sbs_millones",
    "credito_privado_pct_pbi_bcrp"
]

estadisticas = df[
    VARIABLES_ANALISIS
].describe().T

estadisticas = estadisticas[
    [
        "count",
        "mean",
        "std",
        "min",
        "25%",
        "50%",
        "75%",
        "max"
    ]
]

print("\n--- ESTADÍSTICAS DESCRIPTIVAS ---")
print(estadisticas.round(4))

ARCHIVO_ESTADISTICAS = (
    CARPETA_SALIDAS /
    "estadisticas_descriptivas_ALIAGA.csv"
)

estadisticas.to_csv(
    ARCHIVO_ESTADISTICAS,
    encoding="utf-8-sig"
)

print("\nEstadísticas guardadas en:")
print(ARCHIVO_ESTADISTICAS)

# ----------------------------------------------------------
# CRECIMIENTO DEL PBI (%)
# ----------------------------------------------------------

df["crecimiento_pbi"] = (
    df["pbi_desestacionalizado"]
    .pct_change()
    * 100
)

print("\n--- CRECIMIENTO DEL PBI ---")
print(
    "Valores faltantes:",
    df["crecimiento_pbi"].isna().sum()
)

print(
    "Media:",
    round(df["crecimiento_pbi"].mean(), 4)
)

print(
    "Mínimo:",
    round(df["crecimiento_pbi"].min(), 4)
)

print(
    "Máximo:",
    round(df["crecimiento_pbi"].max(), 4)
)

# Crear base sin la primera observación
df_modelo = df.dropna().copy()

print("\n--- BASE PARA EL MODELO ---")
print("Observaciones:", len(df_modelo))
print(
    "Valores faltantes:",
    df_modelo.isna().sum().sum()
)

# ----------------------------------------------------------
# PRUEBAS DE ESTACIONARIEDAD - ADF
# ----------------------------------------------------------

from statsmodels.tsa.stattools import adfuller


def prueba_adf(serie, nombre):
    resultado = adfuller(
        serie.dropna(),
        autolag="AIC"
    )

    print(f"\n--- ADF: {nombre} ---")
    print("Estadístico ADF:", round(resultado[0], 4))
    print("p-valor:", round(resultado[1], 4))
    print("Rezagos utilizados:", resultado[2])

    if resultado[1] < 0.05:
        print("Resultado: serie estacionaria")
    else:
        print("Resultado: serie no estacionaria")


prueba_adf(
    df["credito_privado_pct_pbi_bcrp"],
    "Crédito privado / PBI"
)

prueba_adf(
    df["pbi_desestacionalizado"],
    "PBI desestacionalizado"
)

prueba_adf(
    df["inflacion_ipc"],
    "Inflación"
)

prueba_adf(
    df["tipo_cambio"],
    "Tipo de cambio"
)

# ----------------------------------------------------------
# PRUEBAS ADF EN PRIMERAS DIFERENCIAS
# ----------------------------------------------------------

print("\n========== ADF EN PRIMERAS DIFERENCIAS ==========")

prueba_adf(
    df["credito_privado_pct_pbi_bcrp"].diff(),
    "Δ Crédito privado / PBI"
)

prueba_adf(
    df["pbi_desestacionalizado"].diff(),
    "Δ PBI desestacionalizado"
)

prueba_adf(
    df["tipo_cambio"].diff(),
    "Δ Tipo de cambio"
)

# ----------------------------------------------------------
# PRUEBA DE COINTEGRACIÓN DE ENGLE-GRANGER
# ----------------------------------------------------------

from statsmodels.tsa.stattools import coint

credito_pbi = df_modelo[
    "credito_privado_pct_pbi_bcrp"
]

pbi = df_modelo[
    "pbi_desestacionalizado"
]

resultado_coint = coint(
    pbi,
    credito_pbi
)

estadistico_coint = resultado_coint[0]
p_valor_coint = resultado_coint[1]

print("\n========== COINTEGRACIÓN ENGLE-GRANGER ==========")

print(
    "Estadístico:",
    round(estadistico_coint, 4)
)

print(
    "p-valor:",
    round(p_valor_coint, 4)
)

if p_valor_coint < 0.05:
    print(
        "Resultado: existe evidencia de "
        "cointegración entre Crédito/PBI y PBI."
    )
else:
    print(
        "Resultado: no existe evidencia suficiente de "
        "cointegración entre Crédito/PBI y PBI."
    )

# ----------------------------------------------------------
# PRUEBA DE COINTEGRACIÓN DE JOHANSEN
# ----------------------------------------------------------

from statsmodels.tsa.vector_ar.vecm import coint_johansen

datos_johansen = df_modelo[
    [
        "pbi_desestacionalizado",
        "credito_privado_pct_pbi_bcrp"
    ]
].dropna()

resultado_johansen = coint_johansen(
    datos_johansen,
    det_order=0,
    k_ar_diff=1
)

print("\n========== COINTEGRACIÓN DE JOHANSEN ==========")

print(
    "Estadístico de traza r=0:",
    round(resultado_johansen.lr1[0], 4)
)

print(
    "Valor crítico 5% r=0:",
    round(resultado_johansen.cvt[0, 1], 4)
)

print(
    "Estadístico de traza r<=1:",
    round(resultado_johansen.lr1[1], 4)
)

print(
    "Valor crítico 5% r<=1:",
    round(resultado_johansen.cvt[1, 1], 4)
)

if resultado_johansen.lr1[0] > resultado_johansen.cvt[0, 1]:
    print(
        "Resultado: existe evidencia de al menos "
        "una relación de cointegración."
    )
else:
    print(
        "Resultado: no existe evidencia de "
        "cointegración al 5%."
    )

    # ----------------------------------------------------------
# MODELO EN PRIMERAS DIFERENCIAS
# ----------------------------------------------------------

df_modelo["d_credito_pbi"] = (
    df_modelo["credito_privado_pct_pbi_bcrp"].diff()
)

df_modelo["d_pbi"] = (
    df_modelo["pbi_desestacionalizado"].diff()
)

df_modelo["d_tipo_cambio"] = (
    df_modelo["tipo_cambio"].diff()
)

modelo_diferencias = df_modelo[
    [
        "d_pbi",
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio"
    ]
].dropna()
print("\n========== MODELO EN PRIMERAS DIFERENCIAS ==========")
print("Observaciones:", len(modelo_diferencias))
print("Valores faltantes:", modelo_diferencias.isna().sum().sum())

X = modelo_diferencias[
    [
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio"
    ]
]

X = sm.add_constant(X)

y = modelo_diferencias["d_pbi"]

modelo_ols = sm.OLS(
    y,
    X
).fit()

print(modelo_ols.summary())

# ------------------------------------------------------------
# MODELO COMPLEMENTARIO: CRECIMIENTO TRIMESTRAL DEL PBI
# ------------------------------------------------------------

modelo_crecimiento = df_modelo[
    [
        "crecimiento_pbi",
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio"
    ]
].dropna()

X_crecimiento = modelo_crecimiento[
    [
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio"
    ]
]

X_crecimiento = sm.add_constant(X_crecimiento)

y_crecimiento = modelo_crecimiento["crecimiento_pbi"]

modelo_crecimiento_hac = sm.OLS(
    y_crecimiento,
    X_crecimiento
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4}
)

print(
    "\n========== MODELO: CRECIMIENTO TRIMESTRAL DEL PBI =========="
)

print(modelo_crecimiento_hac.summary())
# ----------------------------------------------------------
# MODELO CON ERRORES ESTÁNDAR ROBUSTOS HAC
# ----------------------------------------------------------

modelo_hac = modelo_ols.get_robustcov_results(
    cov_type="HAC",
    maxlags=4
)

print(
    "\n========== MODELO CON ERRORES ROBUSTOS HAC =========="
)

print(modelo_hac.summary())

# ----------------------------------------------------------
# ROBUSTEZ: CONTROL POR CHOQUE DE LA PANDEMIA
# ----------------------------------------------------------

df_modelo["dummy_covid"] = (
    (df_modelo["anio"] == 2020)
).astype(int)

modelo_covid = df_modelo[
    [
        "d_pbi",
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio",
        "dummy_covid"
    ]
].dropna()

X_covid = modelo_covid[
    [
        "d_credito_pbi",
        "inflacion_ipc",
        "d_tipo_cambio",
        "dummy_covid"
    ]
]

X_covid = sm.add_constant(X_covid)

y_covid = modelo_covid["d_pbi"]

modelo_covid_hac = sm.OLS(
    y_covid,
    X_covid
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4}
)

print(
    "\n========== ROBUSTEZ CON DUMMY COVID-19 =========="
)

print(modelo_covid_hac.summary())

# ----------------------------------------------------------
# GUARDAR RESULTADOS ECONOMÉTRICOS FINALES
# ----------------------------------------------------------

resultados_finales = pd.DataFrame({
    "modelo": [
        "Primeras diferencias HAC",
        "Primeras diferencias HAC + COVID",
        "Crecimiento trimestral del PBI HAC"
    ],
    "coef_credito_pbi": [
        modelo_hac.params[1],
        modelo_covid_hac.params.iloc[1],
        modelo_crecimiento_hac.params.iloc[1]
    ],
    "p_valor_credito_pbi": [
    modelo_hac.pvalues[1],
    modelo_covid_hac.pvalues.iloc[1],
    modelo_crecimiento_hac.pvalues.iloc[1]
],
    "r_cuadrado": [
        modelo_hac.rsquared,
        modelo_covid_hac.rsquared,
        modelo_crecimiento_hac.rsquared
    ],
    "observaciones": [
        int(modelo_hac.nobs),
        int(modelo_covid_hac.nobs),
        int(modelo_crecimiento_hac.nobs)
    ]
})

ARCHIVO_RESULTADOS = (
    CARPETA_SALIDAS /
    "resultados_modelos_ALIAGA.csv"
)

resultados_finales.to_csv(
    ARCHIVO_RESULTADOS,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== RESULTADOS FINALES GUARDADOS ==========")
print(resultados_finales.round(4))
print("\nArchivo:")
print(ARCHIVO_RESULTADOS)

# ------------------------------------------------------------
# GRÁFICO: PROFUNDIZACIÓN FINANCIERA
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    df_modelo["periodo_trimestral"],
    df_modelo["credito_privado_pct_pbi_bcrp"]
)

plt.title(
    "Profundización financiera en el Perú, 2005-2025"
)
plt.xlabel("Periodo")
plt.ylabel("Crédito al sector privado (% del PBI)")

# Mostrar una etiqueta por año
posiciones = range(0, len(df_modelo), 4)

plt.xticks(
    posiciones,
    df_modelo["periodo_trimestral"].iloc[posiciones],
    rotation=45
)

plt.grid(alpha=0.3)
plt.tight_layout()

ARCHIVO_GRAFICO_PROFUNDIZACION = (
    CARPETA_SALIDAS /
    "grafico_profundizacion_financiera_ALIAGA.png"
)

plt.savefig(
    ARCHIVO_GRAFICO_PROFUNDIZACION,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGráfico de profundización financiera guardado en:")
print(ARCHIVO_GRAFICO_PROFUNDIZACION)

# ------------------------------------------------------------
# GRÁFICO: CRECIMIENTO DEL PBI
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    df_modelo["periodo_trimestral"],
    df_modelo["crecimiento_pbi"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "Crecimiento trimestral del PBI del Perú, 2005-2025"
)
plt.xlabel("Periodo")
plt.ylabel("Variación trimestral (%)")

# Mostrar una etiqueta por año
posiciones = range(0, len(df_modelo), 4)

plt.xticks(
    posiciones,
    df_modelo["periodo_trimestral"].iloc[posiciones],
    rotation=45
)

plt.grid(alpha=0.3)
plt.tight_layout()

ARCHIVO_GRAFICO_PBI = (
    CARPETA_SALIDAS /
    "grafico_crecimiento_pbi_ALIAGA.png"
)

plt.savefig(
    ARCHIVO_GRAFICO_PBI,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGráfico de crecimiento del PBI guardado en:")
print(ARCHIVO_GRAFICO_PBI)