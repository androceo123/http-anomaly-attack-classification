# Criterios de conservación de la evidencia experimental

La auditoría distingue los archivos que permiten revisar resultados, ejecutar programas, entender decisiones metodológicas o comprobar integridad. Las colecciones **S01–S14** mantienen identificadores estables en el [inventario](inventario_archivos.csv). Cada registro describe el material examinado y su decisión de conservación; no constituye por sí solo una promesa de disponibilidad en Git.

## Evidencia que se conserva

Se conserva la relación entre documentos de la tesis, código, lanzadores Slurm, configuraciones, métricas, análisis de datos y registros de ejecución. Los modelos, predicciones y checkpoints documentados se identifican en los catálogos, aunque un archivo voluminoso pueda no estar publicado. Las variantes con contenido diferente se distinguen incluso cuando comparten nombre. Los antecedentes de selección tienen su propio estado y no se presentan como las corridas principales del libro.

Los registros históricos de ejecución y sus manifiestos se mantienen junto a las aclaraciones de auditoría. Las tablas que contienen una inconsistencia permanecen identificadas con su interpretación verificada. Las nuevas fichas, catálogos y comprobaciones se reconocen como documentación derivada, sin atribuirles el carácter de resultados de entrenamiento.

## Exclusiones registradas

| Grupo | Archivos | Motivo y alcance |
| --- | ---: | --- |
| Auxiliares de compilación LaTeX de S05 | 16 | Material regenerable; permanecen fuentes, bibliografía y documentos relevantes. |
| Caché Python de S13 | 1 | Bytecode regenerable; no constituye una versión independiente del Python fuente. |
| Lock vacío de la extensión EXP73 | 1 | Estado de bloqueo regenerable, identificado en el inventario. |
| Pesos de candidatos preliminares S13 | 148 | Candidatos no seleccionados localmente o intentos incompletos; se conservan sus tablas y trazas. |

Los **166 registros excluidos** y sus SHA-256 figuran en [archivos_descartados.csv](archivos_descartados.csv). La exclusión de pesos se limita a `*.joblib` en `checkpoints/candidates` y `checkpoints/label_records/candidate_selection` de estas tres búsquedas preliminares:

| Búsqueda | Candidato local conservado |
| --- | --- |
| `resultsOptimo` | `xgboost__w_none` |
| `resultsOptimo_extra_lgbm` | `lightgbm__w_none` |
| `resultsOptimo_extra_lgbm_weights` | `lightgbm__w_cuberoot` |

La decisión retiene los `final_refit`, estados del ganador, modelos finales, configuraciones, tablas de candidatos, métricas, predicciones y logs dentro del conjunto de evidencia conservado. No aplica esta poda a L1 principal, L2 o la variante GPU del job 2625. La tabla final de `resultsOptimo` no presenta un candidato ExtraTrees exitoso; no se asigna a esos pesos un score que la evidencia no contiene. Los resúmenes y hashes de selección constan en [seleccion_y_limpieza_S13.json](seleccion_y_limpieza_S13.json).

Las tablas de candidatos permiten revisar la selección, pero no sustituyen los estimadores serializados para reanudar un entrenamiento. Un candidato cuyo estado no se conservó requiere una nueva ejecución para volver a obtener sus pesos. La disponibilidad concreta de modelos y checkpoints debe comprobarse antes de usar una vía de reanudación.

## Identidad de contenido y copias

El [registro de duplicados](duplicados_fusionados.csv) documenta ocho ocurrencias consolidadas mediante igualdad de SHA-256 y mantiene sus referencias de origen. Una coincidencia de nombre, tamaño o CRC no acredita por sí sola identidad de bytes. Los estados `.partial` y las versiones finales sólo se consideran copias cuando la comprobación de contenido lo demuestra.

La [captura S01 de Slurm](../historial_slurm/evidencia_20260803/) queda íntegra, incluidos los mensajes de error repetidos por job. Esos archivos documentan qué consulta falló en cada ejecución y forman parte de los manifiestos. Tampoco se eliminan `__init__.py` o marcadores estructurales por compartir el hash del contenido vacío con un log.

## Publicación y reproducción

El repositorio publica código, documentación y evidencia seleccionada. Los catálogos permiten distinguir un artefacto documentado de un archivo presente. Los corpus se obtienen desde las [fuentes públicas de datasets](../../03_datasets/README.md); las rutas y dependencias necesarias se describen en la [guía de reproducibilidad](../../07_reproducibilidad/README.md). Los modelos y estados de entrenamiento no se consideran descargables si no existe una ubicación publicada y comprobable.

La auditoría de integridad verifica bytes y relaciones entre artefactos; no acredita por sí sola que un modelo pueda cargarse con cualquier entorno ni que un entrenamiento se reproduzca exactamente. No se reentrenaron modelos durante las comprobaciones documentadas. Los brutos de CSIC, TorpEda y DS-Augmented-v2 y dos scripts preliminares referenciados no aparecieron en las colecciones auditadas; sus ausencias se conservan en las guías de datasets y reproducción.
