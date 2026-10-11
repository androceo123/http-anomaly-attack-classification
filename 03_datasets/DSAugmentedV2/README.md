# WAMM / DS-Augmented-v2

Este corpus aparece en el código y los resultados con el alias `egipcios`. Es una variante de los datasets WAMM de Cyshield. Esta ficha conecta su publicación pública con el formato de entrada utilizado por las corridas de Arandu con Slurm; el corpus y las matrices de entrenamiento se mantienen fuera del repositorio.

## Fuente pública y referencia

Descargar la versión DS-Augmented-v2 desde el [repositorio oficial WAMM de Cyshield](https://github.com/CyShield-Security-R-D/WAMM-Dataset-Repository). El archivo publicado es [**`DS_Augmented_v2.db.xz`**](https://github.com/CyShield-Security-R-D/WAMM-Dataset-Repository/blob/main/DS_Augmented_v2.db.xz), una base SQLite comprimida. La documentación de los autores identifica las versiones DS-Base, DS-Augmented-v1 y DS-Augmented-v2 por separado y declara la licencia CC BY 4.0.

Artículo asociado: Heba Osama y colaboradores, *Enhanced Web Payload Classification Using WAMM: An AI-Based Framework for Dataset Refinement and Model Evaluation*, IEEE Access, 2026, [DOI 10.1109/ACCESS.2026.3685450](https://doi.org/10.1109/ACCESS.2026.3685450). La [publicación técnica de Cyshield](https://seclab.cyshield.com/posts/augmenting-security-datasets-a-technical-methodology-for-modern-threat-simulation/) enlaza las versiones públicas y explica sus transformaciones.

## De la publicación SQLite al CSV de entrada

Los pipelines del proyecto leen `DS_Augmented_v2_csv/combined_data.csv`; ese nombre identifica una **entrada preparada para el experimento**, no un CSV que se deba asumir publicado directamente por los autores. El [cargador de M8](../../05_codigo/pipelines/3datasetsMulticlase2.py) utiliza una columna de petición completa y otra de etiqueta textual:

| Posición esperada | Nombre predeterminado del pipeline | Contenido |
|---|---|---|
| Primera columna | `col1` | Petición HTTP completa, incluyendo método, URI, cabeceras y cuerpo. |
| Segunda columna | `col2` | Etiqueta textual de la clase. |

El README público describe los campos `Full_HTTP_Request` y `Label`. Si la exportación conserva esos encabezados, deben indicarse mediante `--egipcios-request-col` y `--egipcios-label-col`, o prepararse explícitamente como `col1` y `col2`. Revisar el esquema real de la base obtenida antes de exportar; el contenido de una petición puede incluir saltos de línea que requieren un escritor CSV adecuado.

La evidencia histórica incluye el [log de conversión del job 3045](../../02_auditoria/historial_slurm/evidencia_20260803/logs_preservados/por_sacct/job_3045/db_to_csv_3045.out): en el nodo `c1`, con Python 3.11.7, se exportó la tabla `combined_data` de `DS_Augmented_v2.db` a `DS_Augmented_v2_csv/combined_data.csv`, con delimitador coma y **704.665 filas**. Este log documenta una conversión realizada en el clúster; no representa una transformación ejecutada al actualizar estas instrucciones.

## Preparación para Arandu y Slurm

1. Descargar `DS_Augmented_v2.db.xz` de la publicación de Cyshield en el almacenamiento de trabajo del clúster y registrar su revisión, tamaño y SHA-256.
2. Preparar `DS_Augmented_v2.db` a partir del archivo publicado, inspeccionar sus tablas y columnas, y exportar la tabla de peticiones a CSV con las dos columnas anteriores. Para comparar con la conversión histórica, comprobar la existencia y el esquema de `combined_data`.
3. Registrar por separado el hash del CSV resultante, el número de filas, la distribución de etiquetas y el procedimiento de conversión. El mismo total de filas no garantiza igualdad de contenidos ni de etiquetas con la entrada histórica.
4. Configurar la ruta de entrada del lanzador. [M8](../../05_codigo/pipelines/3datasetsMulticlase2.sh) utiliza `EGIPCIOS_RAW_DIR`; la [extensión 73](../../05_codigo/pipelines/3datasetsMulticlase3.sh) utiliza `EGIPCIOS_INPUT`. La ruta histórica es `/home_data/aroman/TFG/waf-ml-starter/egipcios/DS_Augmented_v2_csv/combined_data.csv`.
5. Seguir la [guía del entorno Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md), adaptar rutas y recursos, y enviar la preparación o el entrenamiento con una nueva identidad de job y de corrida.

## Universo y clases de las corridas documentadas

Los artefactos comparados de M7/M8 registran **704.665 eventos**, repartidos en 563.732 de desarrollo y 140.933 de prueba. Utilizan una taxonomía canónica de ocho clases, con las dos clases de comandos fusionadas:

| Clase de M7/M8 | Registros históricos |
|---|---:|
| NORMAL | 493.515 |
| SQLi | 146.086 |
| CommandInjection | 38.711 |
| PathTraversal | 17.718 |
| XSS | 2.894 |
| SSRF | 2.645 |
| SSTI | 1.897 |
| CodeInjection | 1.199 |

La extensión de 73 atributos mantiene separadas `CommandInjection` (2.597) y `OSCommandInjection` (36.114), por lo que utiliza nueve clases. La [revisión de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) documenta estas cifras y sus fuentes. Se conservan los conteos de los experimentos sin sustituirlos por los de una ficha pública posterior; no se ha establecido identidad entre una nueva descarga y el CSV histórico.

## Corridas y alcance de las comparaciones

El [índice experimental](../../04_experimentos/README.md) identifica **M7** con 58 atributos, **M8** con 72 y **EXP73** como extensión de 73 atributos posterior al alcance principal del libro y la presentación. EXP73 no se presenta como una etapa M9 del libro. Cambia representación, número de clases y política de pesos, por lo que no constituye una ablación de una sola variable respecto de M8.

Las curvas de M8 para este corpus se generaron sobre una muestra de 50.000 registros; las métricas globales corresponden al conjunto de prueba de 140.933. Esta diferencia de soporte evita interpretar las curvas como una evaluación sobre una nueva partición completa. Las matrices que se generen deben quedar identificadas por su representación y corrida; no se intercambian por compartir el alias `egipcios`.
