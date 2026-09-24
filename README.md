# Profundización financiera y crecimiento económico en el Perú, 2005-2025

## 1. Información del estudiante

**Estudiante:** Diego Sebastian Aliaga Damián  
**Código de matrícula:** e_2024200481m  
**Curso:** Finanzas I  
**Tema N.° 1:** Profundización financiera y crecimiento económico en el Perú, 2005-2025  

## 2. Descripción del proyecto

El proyecto analiza la relación entre la profundización financiera y el crecimiento económico en el Perú durante el período 2005-2025.

La construcción de la base de datos se realiza mediante extracción automatizada de información de fuentes oficiales. Se utilizan datos del Banco Central de Reserva del Perú (BCRP), mediante BCRPData; del Banco Mundial, mediante la API de World Development Indicators (WDI); y de la Superintendencia de Banca, Seguros y AFP (SBS), mediante descarga programática de boletines estadísticos.

La base mensual comprende 252 observaciones entre enero de 2005 y diciembre de 2025. Para el análisis econométrico, la información es agregada a frecuencia trimestral, obteniéndose 84 observaciones entre 2005T1 y 2025T4.

El análisis considera como indicador principal de profundización financiera el crédito al sector privado como porcentaje del PBI. Asimismo, se utilizan el PBI desestacionalizado, la inflación, el tipo de cambio y los créditos de la banca múltiple como variables complementarias.

## 3. Fuentes de datos

### Banco Central de Reserva del Perú (BCRP)

La información macroeconómica se obtiene mediante extracción automatizada desde BCRPData. Las variables utilizadas son:

- Crédito al sector privado.
- PBI desestacionalizado.
- Inflación medida mediante el IPC.
- Tipo de cambio.
- Crédito al sector privado como porcentaje del PBI.

### Banco Mundial - World Development Indicators (WDI)

Se utiliza la API oficial del Banco Mundial para extraer el indicador:

- `FS.AST.PRVT.GD.ZS`: crédito interno al sector privado como porcentaje del PBI.

Esta información se conserva como fuente oficial complementaria para la profundización financiera.

### Superintendencia de Banca, Seguros y AFP (SBS)

Se realiza la descarga programática de los boletines estadísticos oficiales de banca múltiple de la SBS. A partir de los archivos XLS se extrae la información correspondiente a créditos directos.

La extracción comprende el período enero de 2005 a diciembre de 2025.

**FECHA_INICIO:** 2005-01  
**FECHA_CORTE:** 2025-12
## 4. Orden de ejecución

Los scripts deben ejecutarse en el siguiente orden:

1. `codigo ALIAGA/01_extraccion_api.py`
2. `codigo ALIAGA/02_scraping_web.py`
3. `codigo ALIAGA/03_limpieza_datos.py`
4. `codigo ALIAGA/04_analisis.py`
5. `codigo ALIAGA/05_verificacion_autenticidad.py`
El primer script realiza la extracción automatizada mediante API de información oficial del BCRP y del Banco Mundial (WDI), almacenando los datos crudos.

El segundo script realiza la descarga programática y extracción de información de los boletines estadísticos oficiales de banca múltiple de la SBS.

El tercer script limpia, transforma, valida e integra las distintas fuentes de información. Además, genera las bases procesadas, el diccionario de variables y el hash SHA-256 de la base final.

El cuarto script realiza el análisis estadístico y econométrico. Incluye estadísticas descriptivas, pruebas de estacionariedad ADF, pruebas de cointegración, modelos en primeras diferencias, errores robustos HAC, prueba de robustez con una variable dummy para COVID-19 y generación de gráficos y resultados.

El quinto script verifica la autenticidad y reproducibilidad de la base procesada. Reconstruye las observaciones trimestrales a partir de los datos crudos, compara los resultados con la base final y genera una muestra de 10 observaciones para su verificación.

## 5. Archivos principales

### Datos crudos

Los datos obtenidos directamente de las fuentes oficiales se almacenan en `datos_crudos_ALIAGA`.

Archivos principales:

- `datos_crudos_ALIAGA/datos_crudos_e_2024200481m.csv`
- `datos_crudos_ALIAGA/datos_crudos_e_2024200481m.json`
- `datos_crudos_ALIAGA/datos_sbs_e_2024200481m.csv`
- `datos_crudos_ALIAGA/datos_wdi_e_2024200481m.csv`
- `datos_crudos_ALIAGA/ratio_credito_pbi_bcrp_e_2024200481m.csv`

### Datos procesados

La carpeta `datos_procesados_ALIAGA` contiene las bases generadas después de la limpieza, integración y validación.

Archivos principales:

- `datos_procesados_ALIAGA/datos_mensuales_procesados_e_2024200481m.csv`
- `datos_procesados_ALIAGA/datos_procesados_e_2024200481m.csv`
- `datos_procesados_ALIAGA/datos_wdi_procesados_e_2024200481m.csv`
- `datos_procesados_ALIAGA/diccionario_variables_ALIAGA.csv`
- `datos_procesados_ALIAGA/hash_base_final_ALIAGA.txt`
- `datos_procesados_ALIAGA/comparacion_bcrp_wdi_anual_e_2024200481m.csv`
La base mensual contiene 252 observaciones correspondientes al período 2005-01 a 2025-12. La base trimestral utilizada en el análisis econométrico contiene 84 observaciones, desde 2005T1 hasta 2025T4.

El archivo de comparación BCRP-WDI contiene 20 observaciones anuales para el período 2005-2024 y permite contrastar los indicadores de crédito al sector privado como porcentaje del PBI provenientes de ambas fuentes oficiales.
### Salidas

La carpeta `salidas_ALIAGA` contiene los resultados generados por `04_analisis.py`:

- `estadisticas_descriptivas_ALIAGA.csv`
- `resultados_modelos_ALIAGA.csv`
- `grafico_profundizacion_financiera_ALIAGA.png`
- `grafico_crecimiento_pbi_ALIAGA.png`
- `muestra_verificacion_autenticidad_ALIAGA.csv`
- `evidencia_verificacion_autenticidad_ALIAGA.csv`

Los archivos de verificación de autenticidad documentan una muestra de 10 observaciones de la base final y el resultado de su contraste con los datos crudos utilizados en el proyecto.
## 6. Reproducibilidad

El proyecto utiliza rutas relativas para permitir su ejecución en otros equipos manteniendo la misma estructura de carpetas.

El período de estudio se encuentra definido explícitamente mediante `FECHA_INICIO = 2005-01` y `FECHA_CORTE = 2025-12`.

La extracción de datos se realiza de forma automatizada mediante fuentes oficiales del BCRP, Banco Mundial (WDI) y SBS. Las APIs utilizadas no requieren almacenar credenciales privadas.

Las dependencias necesarias para reproducir el proyecto se encuentran especificadas en:

`requirements.txt`

Para instalarlas:

`pip install -r requirements.txt`

El archivo `.env.example` documenta que el proyecto no requiere claves privadas para las APIs públicas utilizadas.

Los datos crudos se conservan sin modificaciones y las transformaciones necesarias se realizan mediante `03_limpieza_datos.py`.

La integridad de la base procesada final se verifica mediante un hash SHA-256 generado automáticamente.

Adicionalmente, `05_verificacion_autenticidad.py` reconstruye la información trimestral a partir de los datos crudos y la compara con la base procesada final. La verificación realizada sobre las 84 observaciones trimestrales no presenta discrepancias en las variables reconstruidas, y la muestra de 10 observaciones destinada a la comprobación de autenticidad fue verificada satisfactoriamente.
## 7. Integridad de la base procesada

La base trimestral final utilizada para el análisis econométrico es:

**Archivo:** `datos_procesados_e_2024200481m.csv`

La integridad del archivo se verifica mediante SHA-256.

**SHA-256:**

**SHA-256:**

`2e18093fab6fb665ca10fad326f9df7b6fa39feb9ed2ec88498cdb6caa2f55e2`

El hash también se encuentra almacenado en:

`datos_procesados_ALIAGA/hash_base_final_ALIAGA.txt`
## 8. Registro de ejecución

El archivo `log_ejecucion.txt` registra información sobre la ejecución del proyecto y permite documentar el proceso de extracción y procesamiento de los datos.

El registro incluye la fecha de ejecución, las fuentes utilizadas, los períodos disponibles, el número de observaciones, los valores faltantes, la comparación anual BCRP-WDI y el hash SHA-256 de la base procesada final.

**Archivo:**

`log_ejecucion.txt`

## 9. Repositorio

**Repositorio GitHub:** https://github.com/Diego-Aliaga-Damian/ALIAGA-profundizacion-financiera-peru-2005-2025