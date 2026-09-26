# Diego Sebastian Aliaga Damián
# Código de matrícula: e_2024200481m
# Tema N.° 1: Profundización financiera y crecimiento económico en el Perú, 2005-2025
# Fecha de extracción: 20/09/2026

import os
import requests
import pandas as pd
from io import BytesIO
from pathlib import Path
# ----------------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------------

FECHA_INICIO = "2005-01"
FECHA_CORTE = "2025-12"

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos_crudos_ALIAGA"

CARPETA_CRUDOS.mkdir(parents=True, exist_ok=True)
# ----------------------------------------------------------
# CONFIGURACIÓN DE LA FUENTE SBS
# ----------------------------------------------------------

URL_BASE_SBS = (
    "https://intranet2.sbs.gob.pe/estadistica/financiera"
)

CODIGO_CUADRO_SBS = "B-2332"

MESES_SBS = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Setiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

# ----------------------------------------------------------
# FUNCIÓN PARA CONSTRUIR LA URL MENSUAL DE LA SBS
# ----------------------------------------------------------

def construir_url_sbs(anio, mes):
    nombre_mes = MESES_SBS[mes]


    prefijos_sbs = {
        1: "en",
        2: "fe",
        3: "ma",
        4: "ab",
        5: "my",
        6: "jn",
        7: "jl",
        8: "ag",
        9: "se",
        10: "oc",
        11: "no",
        12: "di"
    }

    prefijo_mes = prefijos_sbs[mes]

    nombre_archivo = (
        f"{CODIGO_CUADRO_SBS}-"
        f"{prefijo_mes}{anio}.XLS"
    )

    url = (
        f"{URL_BASE_SBS}/"
        f"{anio}/"
        f"{nombre_mes}/"
        f"{nombre_archivo}"
    )

    return url


        # ----------------------------------------------------------
# FUNCIÓN PARA DESCARGAR UN BOLETÍN MENSUAL DE LA SBS
# ----------------------------------------------------------
def descargar_boletin_sbs(anio, mes):
    url = construir_url_sbs(anio, mes)

    ultimo_error = None

    for intento in range(1, 4):
        try:
            respuesta = requests.get(
                url,
                timeout=120
            )

            respuesta.raise_for_status()

            return respuesta.content, url

        except requests.RequestException as error:
            ultimo_error = error

            print(
                f"   Intento {intento}/3 fallido:",
                error
            )

    raise RuntimeError(
        f"No se pudo descargar el boletín después "
        f"de 3 intentos. Último error: {ultimo_error}"
    )


# ----------------------------------------------------------
# FUNCIÓN PARA BUSCAR TEXTO DENTRO DE UNA HOJA
# ----------------------------------------------------------

def buscar_fila_texto(datos, texto):
    for indice, fila in datos.iterrows():
        for valor in fila:
            if pd.notna(valor) and texto.lower() in str(valor).lower():
                return indice

    return None


# ----------------------------------------------------------
# FUNCIÓN PARA ENCONTRAR LA HOJA DE CRÉDITOS
# ----------------------------------------------------------

def encontrar_hoja_creditos(contenido_excel):
    archivo_temporal = BytesIO(contenido_excel)

    excel = pd.ExcelFile(archivo_temporal)

    for nombre_hoja in excel.sheet_names:
        archivo_temporal.seek(0)

        datos = pd.read_excel(
            archivo_temporal,
            sheet_name=nombre_hoja,
            header=None
        )

        fila_creditos = buscar_fila_texto(
            datos,
            "Créditos Directos"
        )

        fila_depositos = buscar_fila_texto(
            datos,
            "Depósitos Totales"
        )

        if fila_creditos is not None and fila_depositos is not None:
            return datos, nombre_hoja, fila_creditos, fila_depositos

    return None, None, None, None

# ----------------------------------------------------------
# FUNCIÓN PARA EXTRAER LOS CRÉDITOS DIRECTOS
# ----------------------------------------------------------

def extraer_creditos_sbs(contenido_excel):
    datos, nombre_hoja, fila_creditos, fila_depositos = (
        encontrar_hoja_creditos(contenido_excel)
    )

    if datos is None:
        raise ValueError(
            "No se encontró la sección de Créditos Directos."
        )

    bloque_creditos = datos.iloc[
        fila_creditos + 1:fila_depositos
    ].copy()

    # La columna 3 contiene los montos en miles de soles
    bloque_creditos["monto"] = pd.to_numeric(
        bloque_creditos.iloc[:, 3],
        errors="coerce"
    )

    entidades = bloque_creditos[
        bloque_creditos["monto"].notna()
    ].copy()

    total_miles_soles = entidades["monto"].sum()
    total_millones_soles = total_miles_soles / 1000

    return {
        "hoja": nombre_hoja,
        "numero_entidades": len(entidades),
        "creditos_sbs_millones": total_millones_soles
    }

# ----------------------------------------------------------
# PREPARACIÓN DE LA EXTRACCIÓN HISTÓRICA
# ----------------------------------------------------------

resultados_sbs = []
errores_sbs = []

periodos = pd.period_range(
    start=FECHA_INICIO,
    end=FECHA_CORTE,
    freq="M"
)

print("\n--- EXTRACCIÓN HISTÓRICA SBS ---")
print("Periodo inicial:", FECHA_INICIO)
print("Periodo final:", FECHA_CORTE)
print("Número de meses programados:", len(periodos))

# ----------------------------------------------------------
# DESCARGA Y EXTRACCIÓN DE LOS 252 MESES
# ----------------------------------------------------------

for numero, periodo in enumerate(periodos, start=1):
    anio = periodo.year
    mes = periodo.month
    fecha = str(periodo)

    print(
        f"[{numero}/{len(periodos)}] "
        f"Procesando {fecha}..."
    )

    try:
        contenido_excel, url = descargar_boletin_sbs(
            anio,
            mes
        )

        resultado = extraer_creditos_sbs(
            contenido_excel
        )

        resultados_sbs.append({
            "fecha": fecha,
            "creditos_sbs_millones":
                resultado["creditos_sbs_millones"],
            "numero_entidades_sbs":
                resultado["numero_entidades"],
            "hoja_sbs":
                resultado["hoja"],
            "url_sbs": url
        })

        # Guardar avance cada 12 meses
        if numero % 12 == 0:
            archivo_avance = os.path.join(
                CARPETA_CRUDOS,
                "avance_sbs_e_2024200481m.csv"
            )

            pd.DataFrame(resultados_sbs).to_csv(
                archivo_avance,
                index=False,
                encoding="utf-8-sig"
            )

            print(
                f"   Avance guardado: {numero}/"
                f"{len(periodos)} meses"
            )

        print(
            "   OK - Créditos:",
            round(
                resultado["creditos_sbs_millones"],
                3
            ),
            "millones de S/"
        )

    except Exception as error:
        errores_sbs.append({
            "fecha": fecha,
            "error": str(error)
        })

        print(
            "   ERROR:",
            error
        )
# ----------------------------------------------------------
# GUARDAR RESULTADOS DE LA EXTRACCIÓN SBS
# ----------------------------------------------------------

df_sbs = pd.DataFrame(resultados_sbs)

ARCHIVO_SBS_CSV = os.path.join(
    CARPETA_CRUDOS,
    "datos_sbs_e_2024200481m.csv"
)

df_sbs.to_csv(
    ARCHIVO_SBS_CSV,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- RESUMEN FINAL SBS ---")
print("Meses programados:", len(periodos))
print("Meses extraídos correctamente:", len(resultados_sbs))
print("Meses con error:", len(errores_sbs))
print("Archivo guardado en:")
print(ARCHIVO_SBS_CSV)


# Guardar registro de errores de la ejecución actual
ARCHIVO_ERRORES = os.path.join(
    CARPETA_CRUDOS,
    "errores_sbs_e_2024200481m.csv"
)

if errores_sbs:
    df_errores = pd.DataFrame(errores_sbs)

    df_errores.to_csv(
        ARCHIVO_ERRORES,
        index=False,
        encoding="utf-8-sig"
    )

    print("Registro de errores guardado en:")
    print(ARCHIVO_ERRORES)

else:
    # Eliminar un registro antiguo si la ejecución actual no tuvo errores
    if os.path.exists(ARCHIVO_ERRORES):
        os.remove(ARCHIVO_ERRORES)

    print("Errores de extracción SBS: 0")