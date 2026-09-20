# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 19/09/2026

import csv
from pathlib import Path
import statistics
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

# Definir las rutas del proyecto
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_PROCESADOS = CARPETA_PROYECTO / "datos_procesados_ALIAGA"
CARPETA_SALIDAS = CARPETA_PROYECTO / "salidas_ALIAGA"

# Archivo que será utilizado para el análisis
ARCHIVO_DATOS = (
    CARPETA_PROCESADOS / "datos_procesados_e_2024200481m.csv"
)

print("Base de datos para el análisis:")
print(ARCHIVO_DATOS)

# Leer la base de datos procesada
with open(ARCHIVO_DATOS, "r", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    datos = list(lector)

print("\n--- VERIFICACIÓN DE LA BASE PARA EL ANÁLISIS ---")
print("Número de observaciones:", len(datos))
print("Columnas:", lector.fieldnames)
print("Primer periodo:", datos[0]["periodo"])
print("Último periodo:", datos[-1]["periodo"])

# Convertir las variables económicas a valores numéricos
for fila in datos:
    fila["crecimiento_pbi"] = float(fila["crecimiento_pbi"])
    fila["liquidez_pbi"] = float(fila["liquidez_pbi"])
    fila["credito_mn_pbi"] = float(fila["credito_mn_pbi"])
    fila["credito_total_pbi"] = float(fila["credito_total_pbi"])

print("\n--- VERIFICACIÓN DE TIPOS DE DATOS ---")
print("crecimiento_pbi:", type(datos[0]["crecimiento_pbi"]).__name__)
print("liquidez_pbi:", type(datos[0]["liquidez_pbi"]).__name__)
print("credito_mn_pbi:", type(datos[0]["credito_mn_pbi"]).__name__)
print("credito_total_pbi:", type(datos[0]["credito_total_pbi"]).__name__)

# Separar las variables económicas
crecimiento_pbi = [fila["crecimiento_pbi"] for fila in datos]
liquidez_pbi = [fila["liquidez_pbi"] for fila in datos]
credito_mn_pbi = [fila["credito_mn_pbi"] for fila in datos]
credito_total_pbi = [fila["credito_total_pbi"] for fila in datos]

# Función para calcular estadísticas descriptivas
def estadisticas_descriptivas(nombre, valores):
    print(f"\n--- {nombre} ---")
    print("Media:", round(statistics.mean(valores), 4))
    print("Mínimo:", round(min(valores), 4))
    print("Máximo:", round(max(valores), 4))
    print("Desviación estándar:", round(statistics.stdev(valores), 4))

print("\n========== ESTADÍSTICAS DESCRIPTIVAS ==========")

estadisticas_descriptivas(
    "Crecimiento del PBI",
    crecimiento_pbi
)

estadisticas_descriptivas(
    "Liquidez / PBI",
    liquidez_pbi
)

estadisticas_descriptivas(
    "Crédito MN / PBI",
    credito_mn_pbi
)

estadisticas_descriptivas(
    "Crédito total / PBI",
    credito_total_pbi
)

# Crear la carpeta de salidas si no existiera
CARPETA_SALIDAS.mkdir(parents=True, exist_ok=True)

# Archivo para guardar las estadísticas descriptivas
ARCHIVO_ESTADISTICAS = (
    CARPETA_SALIDAS / "estadisticas_descriptivas_ALIAGA.csv"
)

# Preparar los resultados
resultados_estadisticos = [
    {
        "variable": "crecimiento_pbi",
        "media": statistics.mean(crecimiento_pbi),
        "minimo": min(crecimiento_pbi),
        "maximo": max(crecimiento_pbi),
        "desviacion_estandar": statistics.stdev(crecimiento_pbi)
    },
    {
        "variable": "liquidez_pbi",
        "media": statistics.mean(liquidez_pbi),
        "minimo": min(liquidez_pbi),
        "maximo": max(liquidez_pbi),
        "desviacion_estandar": statistics.stdev(liquidez_pbi)
    },
    {
        "variable": "credito_mn_pbi",
        "media": statistics.mean(credito_mn_pbi),
        "minimo": min(credito_mn_pbi),
        "maximo": max(credito_mn_pbi),
        "desviacion_estandar": statistics.stdev(credito_mn_pbi)
    },
    {
        "variable": "credito_total_pbi",
        "media": statistics.mean(credito_total_pbi),
        "minimo": min(credito_total_pbi),
        "maximo": max(credito_total_pbi),
        "desviacion_estandar": statistics.stdev(credito_total_pbi)
    }
]

# Guardar las estadísticas descriptivas
with open(
    ARCHIVO_ESTADISTICAS,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:
    columnas = [
        "variable",
        "media",
        "minimo",
        "maximo",
        "desviacion_estandar"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=columnas
    )

    escritor.writeheader()
    escritor.writerows(resultados_estadisticos)

print("\nEstadísticas descriptivas guardadas en:")
print(ARCHIVO_ESTADISTICAS)

# Calcular correlaciones entre crecimiento económico
# e indicadores de profundización financiera

correlacion_liquidez = statistics.correlation(
    crecimiento_pbi,
    liquidez_pbi
)

correlacion_credito_mn = statistics.correlation(
    crecimiento_pbi,
    credito_mn_pbi
)

correlacion_credito_total = statistics.correlation(
    crecimiento_pbi,
    credito_total_pbi
)

print("\n========== CORRELACIONES ==========")

print(
    "Crecimiento PBI - Liquidez/PBI:",
    round(correlacion_liquidez, 4)
)

print(
    "Crecimiento PBI - Crédito MN/PBI:",
    round(correlacion_credito_mn, 4)
)

print(
    "Crecimiento PBI - Crédito total/PBI:",
    round(correlacion_credito_total, 4)
)

# Guardar las correlaciones
ARCHIVO_CORRELACIONES = (
    CARPETA_SALIDAS / "correlaciones_ALIAGA.csv"
)

resultados_correlaciones = [
    {
        "variable_1": "crecimiento_pbi",
        "variable_2": "liquidez_pbi",
        "correlacion": correlacion_liquidez
    },
    {
        "variable_1": "crecimiento_pbi",
        "variable_2": "credito_mn_pbi",
        "correlacion": correlacion_credito_mn
    },
    {
        "variable_1": "crecimiento_pbi",
        "variable_2": "credito_total_pbi",
        "correlacion": correlacion_credito_total
    }
]

with open(
    ARCHIVO_CORRELACIONES,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:

    columnas_correlacion = [
        "variable_1",
        "variable_2",
        "correlacion"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=columnas_correlacion
    )

    escritor.writeheader()
    escritor.writerows(resultados_correlaciones)

print("\nCorrelaciones guardadas en:")
print(ARCHIVO_CORRELACIONES)

# Crear gráfico de evolución del crecimiento del PBI
periodos = [fila["periodo"] for fila in datos]

plt.figure(figsize=(12, 6))

plt.plot(
    periodos,
    crecimiento_pbi
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title("Crecimiento del PBI del Perú, 2005-2025")
plt.xlabel("Periodo")
plt.ylabel("Variación porcentual interanual (%)")

# Mostrar una etiqueta por año para evitar saturación
posiciones = list(range(0, len(periodos), 4))
etiquetas = [periodos[i][:4] for i in posiciones]

plt.xticks(
    posiciones,
    etiquetas,
    rotation=45
)

plt.grid(alpha=0.3)
plt.tight_layout()

# Guardar el gráfico
ARCHIVO_GRAFICO_PBI = (
    CARPETA_SALIDAS / "grafico_crecimiento_pbi_ALIAGA.png"
)

plt.savefig(
    ARCHIVO_GRAFICO_PBI,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGráfico de crecimiento del PBI guardado en:")
print(ARCHIVO_GRAFICO_PBI)

# Crear gráfico de los indicadores de profundización financiera
plt.figure(figsize=(12, 6))

plt.plot(
    periodos,
    liquidez_pbi,
    label="Liquidez / PBI"
)

plt.plot(
    periodos,
    credito_mn_pbi,
    label="Crédito MN / PBI"
)

plt.plot(
    periodos,
    credito_total_pbi,
    label="Crédito total / PBI"
)

plt.title("Indicadores de profundización financiera en el Perú, 2005-2025")
plt.xlabel("Periodo")
plt.ylabel("Porcentaje del PBI (%)")

# Mostrar una etiqueta por año
plt.xticks(
    posiciones,
    etiquetas,
    rotation=45
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# Guardar el gráfico
ARCHIVO_GRAFICO_FINANCIERO = (
    CARPETA_SALIDAS / "grafico_profundizacion_financiera_ALIAGA.png"
)

plt.savefig(
    ARCHIVO_GRAFICO_FINANCIERO,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGráfico de profundización financiera guardado en:")
print(ARCHIVO_GRAFICO_FINANCIERO)

# Matriz de correlaciones de las variables económicas
variables = {
    "crecimiento_pbi": crecimiento_pbi,
    "liquidez_pbi": liquidez_pbi,
    "credito_mn_pbi": credito_mn_pbi,
    "credito_total_pbi": credito_total_pbi
}

nombres_variables = list(variables.keys())

print("\n========== MATRIZ DE CORRELACIONES ==========")

for variable_1 in nombres_variables:
    fila_resultados = []

    for variable_2 in nombres_variables:
        correlacion = statistics.correlation(
            variables[variable_1],
            variables[variable_2]
        )

        fila_resultados.append(round(correlacion, 4))

    print(variable_1, ":", fila_resultados)

    # ============================================================
# MODELO 1: CRECIMIENTO DEL PBI Y LIQUIDEZ / PBI
# ============================================================

# Variable dependiente (Y)
Y = crecimiento_pbi

# Variable explicativa (X)
X_liquidez = liquidez_pbi

# Agregar una constante para estimar el intercepto beta_0
X_liquidez_constante = sm.add_constant(X_liquidez)

# Estimar el modelo mediante Mínimos Cuadrados Ordinarios (MCO)
modelo_liquidez = sm.OLS(
    Y,
    X_liquidez_constante
).fit()

print("\n========== MODELO 1: LIQUIDEZ / PBI ==========")
print(modelo_liquidez.summary())

# ============================================================
# MODELO 2: CRECIMIENTO DEL PBI Y CRÉDITO MN / PBI
# ============================================================

# Variable explicativa
X_credito_mn = credito_mn_pbi

# Agregar constante
X_credito_mn_constante = sm.add_constant(X_credito_mn)

# Estimar mediante Mínimos Cuadrados Ordinarios
modelo_credito_mn = sm.OLS(
    Y,
    X_credito_mn_constante
).fit()

print("\n========== MODELO 2: CRÉDITO MN / PBI ==========")
print(modelo_credito_mn.summary())

# ============================================================
# MODELO 3: CRECIMIENTO DEL PBI Y CRÉDITO TOTAL / PBI
# ============================================================

# Variable explicativa
X_credito_total = credito_total_pbi

# Agregar constante
X_credito_total_constante = sm.add_constant(X_credito_total)

# Estimar mediante Mínimos Cuadrados Ordinarios
modelo_credito_total = sm.OLS(
    Y,
    X_credito_total_constante
).fit()

print("\n========== MODELO 3: CRÉDITO TOTAL / PBI ==========")
print(modelo_credito_total.summary())

# ============================================================
# GUARDAR RESULTADOS DE LOS TRES MODELOS
# ============================================================

ARCHIVO_MODELOS = (
    CARPETA_SALIDAS / "resultados_modelos_ALIAGA.csv"
)

resultados_modelos = [
    {
        "modelo": "Liquidez / PBI",
        "intercepto": modelo_liquidez.params[0],
        "coeficiente": modelo_liquidez.params[1],
        "p_valor": modelo_liquidez.pvalues[1],
        "r_cuadrado": modelo_liquidez.rsquared,
        "r_cuadrado_ajustado": modelo_liquidez.rsquared_adj,
        "prob_f": modelo_liquidez.f_pvalue,
        "durbin_watson": sm.stats.stattools.durbin_watson(
            modelo_liquidez.resid
        )
    },
    {
        "modelo": "Crédito MN / PBI",
        "intercepto": modelo_credito_mn.params[0],
        "coeficiente": modelo_credito_mn.params[1],
        "p_valor": modelo_credito_mn.pvalues[1],
        "r_cuadrado": modelo_credito_mn.rsquared,
        "r_cuadrado_ajustado": modelo_credito_mn.rsquared_adj,
        "prob_f": modelo_credito_mn.f_pvalue,
        "durbin_watson": sm.stats.stattools.durbin_watson(
            modelo_credito_mn.resid
        )
    },
    {
        "modelo": "Crédito total / PBI",
        "intercepto": modelo_credito_total.params[0],
        "coeficiente": modelo_credito_total.params[1],
        "p_valor": modelo_credito_total.pvalues[1],
        "r_cuadrado": modelo_credito_total.rsquared,
        "r_cuadrado_ajustado": modelo_credito_total.rsquared_adj,
        "prob_f": modelo_credito_total.f_pvalue,
        "durbin_watson": sm.stats.stattools.durbin_watson(
            modelo_credito_total.resid
        )
    }
]

columnas_modelos = [
    "modelo",
    "intercepto",
    "coeficiente",
    "p_valor",
    "r_cuadrado",
    "r_cuadrado_ajustado",
    "prob_f",
    "durbin_watson"
]

with open(
    ARCHIVO_MODELOS,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:

    escritor = csv.DictWriter(
        archivo,
        fieldnames=columnas_modelos
    )

    escritor.writeheader()
    escritor.writerows(resultados_modelos)

print("\nResultados de los modelos guardados en:")
print(ARCHIVO_MODELOS)

# ============================================================
# PRUEBA DE AUTOCORRELACIÓN DE BREUSCH-GODFREY
# ============================================================

# Aplicar la prueba con 4 rezagos por tratarse de datos trimestrales
bg_liquidez = acorr_breusch_godfrey(
    modelo_liquidez,
    nlags=4
)

bg_credito_mn = acorr_breusch_godfrey(
    modelo_credito_mn,
    nlags=4
)

bg_credito_total = acorr_breusch_godfrey(
    modelo_credito_total,
    nlags=4
)

print("\n========== PRUEBA BREUSCH-GODFREY ==========")

print(
    "Liquidez/PBI - LM:",
    round(bg_liquidez[0], 4),
    "- p-valor:",
    round(bg_liquidez[1], 4)
)

print(
    "Crédito MN/PBI - LM:",
    round(bg_credito_mn[0], 4),
    "- p-valor:",
    round(bg_credito_mn[1], 4)
)

print(
    "Crédito total/PBI - LM:",
    round(bg_credito_total[0], 4),
    "- p-valor:",
    round(bg_credito_total[1], 4)
)

# ============================================================
# MODELO 1 CON ERRORES ESTÁNDAR HAC / NEWEY-WEST
# ============================================================

modelo_liquidez_hac = modelo_liquidez.get_robustcov_results(
    cov_type="HAC",
    maxlags=4
)

print("\n========== MODELO 1: LIQUIDEZ/PBI - HAC ==========")
print(modelo_liquidez_hac.summary())

# ============================================================
# MODELOS 2 Y 3 CON ERRORES ESTÁNDAR HAC / NEWEY-WEST
# ============================================================

modelo_credito_mn_hac = modelo_credito_mn.get_robustcov_results(
    cov_type="HAC",
    maxlags=4
)

modelo_credito_total_hac = modelo_credito_total.get_robustcov_results(
    cov_type="HAC",
    maxlags=4
)

print("\n========== MODELO 2: CRÉDITO MN/PBI - HAC ==========")
print(modelo_credito_mn_hac.summary())

print("\n========== MODELO 3: CRÉDITO TOTAL/PBI - HAC ==========")
print(modelo_credito_total_hac.summary())

# ============================================================
# GUARDAR RESULTADOS DE LOS MODELOS CON HAC
# ============================================================

ARCHIVO_MODELOS_HAC = (
    CARPETA_SALIDAS / "resultados_modelos_HAC_ALIAGA.csv"
)

resultados_hac = [
    {
        "modelo": "Liquidez / PBI",
        "coeficiente": modelo_liquidez_hac.params[1],
        "error_estandar": modelo_liquidez_hac.bse[1],
        "t": modelo_liquidez_hac.tvalues[1],
        "p_valor": modelo_liquidez_hac.pvalues[1],
        "ic_95_inferior": modelo_liquidez_hac.conf_int()[1][0],
        "ic_95_superior": modelo_liquidez_hac.conf_int()[1][1]
    },
    {
        "modelo": "Crédito MN / PBI",
        "coeficiente": modelo_credito_mn_hac.params[1],
        "error_estandar": modelo_credito_mn_hac.bse[1],
        "t": modelo_credito_mn_hac.tvalues[1],
        "p_valor": modelo_credito_mn_hac.pvalues[1],
        "ic_95_inferior": modelo_credito_mn_hac.conf_int()[1][0],
        "ic_95_superior": modelo_credito_mn_hac.conf_int()[1][1]
    },
    {
        "modelo": "Crédito total / PBI",
        "coeficiente": modelo_credito_total_hac.params[1],
        "error_estandar": modelo_credito_total_hac.bse[1],
        "t": modelo_credito_total_hac.tvalues[1],
        "p_valor": modelo_credito_total_hac.pvalues[1],
        "ic_95_inferior": modelo_credito_total_hac.conf_int()[1][0],
        "ic_95_superior": modelo_credito_total_hac.conf_int()[1][1]
    }
]

columnas_hac = [
    "modelo",
    "coeficiente",
    "error_estandar",
    "t",
    "p_valor",
    "ic_95_inferior",
    "ic_95_superior"
]

with open(
    ARCHIVO_MODELOS_HAC,
    "w",
    newline="",
    encoding="utf-8-sig"
) as archivo:

    escritor = csv.DictWriter(
        archivo,
        fieldnames=columnas_hac
    )

    escritor.writeheader()
    escritor.writerows(resultados_hac)

print("\nResultados HAC guardados en:")
print(ARCHIVO_MODELOS_HAC)