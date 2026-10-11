# SR-BH 2020 / Harvard

Este corpus aparece en los artefactos como `harvard`, `SRBH2020` o SR-BH. Esta ficha documenta su fuente pública y la relación entre la entrada histórica, las transformaciones y las ejecuciones en Arandu con Slurm. El CSV completo se descarga por separado y se mantiene fuera del repositorio.

## Fuente pública

Descargar **SR-BH 2020 multi-label dataset** desde [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/OGOIXX), identificado por el [DOI 10.7910/DVN/OGOIXX](https://doi.org/10.7910/DVN/OGOIXX). La [ficha de la institución de los autores](https://investigacion.unir.net/documentos/668fc479b9e7c03b01bde810) registra la versión 1.2, publicada en 2022 bajo CC0 1.0. El año 2020 identifica la recolección de las peticiones.

La entrada esperada por los pipelines es `data_capec_multilabel.csv`, con campos HTTP, NORMAL y las etiquetas CAPEC. Registrar la versión descargada, el nombre del archivo, su tamaño y SHA-256 antes de procesarlo. Las métricas históricas solo identifican una entrada concreta cuando existe evidencia de su contenido o de su hash.

## Identidad de la entrada histórica

El [perfil auditado](../../02_auditoria/datasets_y_multiclase/sr_bh_raw_profile.json) documenta **907.815 filas y 38 columnas**, con 525.195 eventos normales y 382.620 con al menos una CAPEC. La cifra de 907.814 citada por la fuente se mantiene diferenciada de este recuento.

| Identificador | Valor registrado |
|---|---|
| Archivo | `data_capec_multilabel.csv` |
| Tamaño | 436.437.661 bytes |
| SHA-256 | `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910` |
| Ruta histórica en Arandu | `/home_data/aroman/TFG/waf-ml-starter/data/raw/harvard/data_capec_multilabel.csv` |

El hash también figura en `input_fingerprints` de la [configuración histórica de la extensión 73](../../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/3datasetsMulticlase3/multiclase/harvard/run_config.json). Este registro se conserva para comparar identidades; no afirma que el archivo esté publicado en esta carpeta ni que la descarga actual produzca automáticamente el mismo hash.

## Preparación para Arandu y Slurm

1. Descargar el CSV de Dataverse en el almacenamiento de trabajo accesible desde los nodos del clúster.
2. Verificar los encabezados contra el [perfil de campos](../../02_auditoria/datasets_y_multiclase/sr_bh_raw_profile.json), registrar el hash y elegir explícitamente la etapa multiclase o multietiqueta.
3. Aplicar su parser, filtros, orden de atributos y taxonomía. Las etiquetas CAPEC pueden coexistir en un evento; las familias multiclase son transformaciones posteriores, no columnas intercambiables del original.
4. Configurar `HARVARD_RAW_DIR` cuando lo admita el lanzador, o su argumento de entrada correspondiente. Seguir la [guía del entorno Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md) para enviar el trabajo y conservar una nueva configuración, particiones y logs.

## Universos y objetivos

La selección multiclase Top14 conserva 902.411 eventos y descarta 5.404 de las combinaciones no incluidas. Top11 y Top10 mantienen esas filas y fusionan categorías. M1, en cambio, usa nueve familias y 907.815 eventos; no debe atribuírsele retrospectivamente el filtro Top14. La [evidencia de M1–M3](../../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.md) identifica estas diferencias.

L1 trabaja con eventos. L2 excluye dos peticiones vacías y agrupa los 907.813 eventos restantes en **542.990 huellas** de quince campos HTTP, uniendo las CAPEC mediante OR. Sus pruebas corresponden a 181.563 eventos y 108.598 grupos, respectivamente. Los denominadores no deben intercambiarse, y las 902.411 filas Top14 no representan una deduplicación L2.

CAPEC-248 tiene un solo positivo en la entrada histórica y se excluye como objetivo de las evaluaciones L1/L2 de doce etiquetas. Los conteos marginales de CAPEC se solapan y no se suman como clases mutuamente excluyentes. El [catálogo general](../README.md) conserva los marginales, las fusiones multiclase y los tamaños completos de las particiones.

## Análisis, corridas y auditoría

- [Revisión de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md): universos, taxonomías y cambios de las etapas M1–M8.
- [Auditoría recalculada de la planilla](../../02_auditoria/datasets_y_multiclase/S10_auditoria_excel_recalculado.json): repeticiones y conflictos de etiquetas.
- [Evidencia multietiqueta](../../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md): huellas, particiones y relación entre predicciones y métricas.
- [Huella de quince campos](../esquemas/huella_peticion_15_campos.json): identidad de petición, distinta de comparar todos los campos del evento.
- [Índice experimental](../../04_experimentos/README.md): etapas multiclase, L1 fixed30, L2 request90 y el antecedente GPU/job 2625, identificado por separado.

Las reconstrucciones de particiones fechadas en octubre de 2026 son verificaciones posteriores. No sustituyen a listas históricas completas de entrenamiento, selección y calibración, que no están disponibles. Una nueva preparación debe mantener su propia identidad de datos y de corrida.
