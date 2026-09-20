# Profundización financiera y crecimiento económico en el Perú, 2005-2025

## 1. Información del estudiante

**Estudiante:** Diego Sebastian Aliaga Damián  
**Código de matrícula:** e_2024200481m  
**Curso:** Finanzas I  
**Tema N.° 1:** Profundización financiera y crecimiento económico en el Perú, 2005-2025  

## 2. Descripción del proyecto

El proyecto analiza la relación entre la profundización financiera y el crecimiento económico en el Perú durante el período 2005-2025.

La base de datos fue construida mediante extracción automatizada de información oficial del Banco Central de Reserva del Perú (BCRP), utilizando BCRPData.

La frecuencia utilizada es trimestral y comprende desde 2005T1 hasta 2025T4.

## 3. Fuente de datos

**Fuente:** Banco Central de Reserva del Perú - BCRPData.

**Series utilizadas:**

- PN03500MQ: Crédito al Sector Privado - Total (% del PBI).
- PN03497MQ: Liquidez - Total (% del PBI).
- PN03498MQ: Crédito al Sector Privado - Moneda Nacional (% del PBI).
- PN02507AQ: Producto Bruto Interno - variación porcentual interanual.

**FECHA_INICIO:** 2005-1  
**FECHA_CORTE:** 2025-4

**Endpoint utilizado:**

https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN03500MQ-PN03497MQ-PN03498MQ-PN02507AQ/json/2005-1/2025-4/esp

## 4. Orden de ejecución

Los scripts deben ejecutarse en el siguiente orden:

1. `codigo ALIAGA/01_extraccion_api.py`
2. `codigo ALIAGA/03_limpieza_datos.py`
3. `codigo ALIAGA/04_analisis.py`

El primer script realiza la extracción automatizada desde BCRPData y almacena los datos crudos.

El segundo script transforma y valida la información, genera la base procesada y el diccionario de variables.

El tercer script realiza el análisis estadístico y econométrico y genera las salidas del proyecto.

No se utiliza `02_scraping_web.py`, debido a que para este proyecto se emplea una única vía automatizada de extracción mediante API.

## 5. Archivos principales

### Datos crudos

- `datos_crudos_ALIAGA/datos_crudos_e_2024200481m.json`
- `datos_crudos_ALIAGA/datos_crudos_e_2024200481m.csv`

### Datos procesados

- `datos_procesados_ALIAGA/datos_procesados_e_2024200481m.csv`
- `datos_procesados_ALIAGA/diccionario_variables_ALIAGA.csv`

### Salidas

La carpeta `salidas_ALIAGA` contiene las estadísticas descriptivas, correlaciones, gráficos y resultados de los modelos econométricos.

## 6. Reproducibilidad

El proyecto utiliza rutas relativas para facilitar su ejecución en otros equipos.

Las fechas de inicio y corte se encuentran definidas explícitamente en el código.

La API utilizada no requiere clave de acceso.

Las dependencias necesarias se encuentran en:

`requirements.txt`

Para instalarlas:

`pip install -r requirements.txt`

## 7. Integridad de la base procesada

**Archivo:** `datos_procesados_e_2024200481m.csv`

**SHA-256:**

`17d9103817d4949ccd39d228d462dcc4e5dfc0fcb0ffa01d2af0db8bf12f891b`

## 8. Registro de ejecución

El archivo `log_ejecucion.txt` registra la ejecución de la extracción, incluyendo fecha y hora, estado HTTP, número de observaciones, variables, valores faltantes, período analizado y endpoint utilizado.

## 9. Repositorio

**Repositorio GitHub:** PENDIENTE