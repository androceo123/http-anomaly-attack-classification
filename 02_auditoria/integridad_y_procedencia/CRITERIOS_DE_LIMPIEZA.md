# Criterios y resultado de la limpieza

La organización cubre los **13 ZIP completos**, un Excel independiente y los dos documentos rectores aportados por el autor. No se encontraron archivos comprimidos anidados dentro de los paquetes. Cada entrada tiene fuente, ruta original, tamaño, SHA-256, clasificación y decisión en el inventario.

## Qué se conservó

Se mantienen documentos rectores e informes, código y lanzadores originales, configuraciones, métricas, predicciones, modelos finales, estados de las corridas principales, análisis de datos y evidencia de ejecución. Las variantes con contenido distinto se conservan aunque compartan nombre. Los antecedentes de selección se distinguen de las etapas que presentan el libro y la defensa.

Los originales no se reescribieron. Los nuevos README, catálogos y verificaciones están fechados en 2026 y se identifican como documentación de esta organización. Las tablas históricas que contienen una inconsistencia permanecen junto a su explicación en la auditoría.

## Qué se descartó

| Grupo | Archivos | Motivo |
| --- | ---: | --- |
| Auxiliares de compilación LaTeX de S05 | 16 | Son regenerables; permanecen fuentes, bibliografía y documentos relevantes. |
| Caché Python de S13 | 1 | Bytecode regenerable; se conserva el Python fuente. |
| Lock vacío de la extensión EXP73 | 1 | Archivo de bloqueo regenerable; se conserva su procedencia en el inventario. |
| Pesos de candidatos preliminares S13 | 148 | No son los candidatos seleccionados localmente o pertenecen a intentos incompletos. Se conservan sus tablas y trazas. |

Los **166 descartes** suman **5.851.709.924 bytes**. Cada uno está registrado en [archivos_descartados.csv](archivos_descartados.csv), incluido su SHA-256. El descarte de pesos se limita a `*.joblib` en `checkpoints/candidates` y `checkpoints/label_records/candidate_selection` de las tres búsquedas preliminares siguientes:

| Búsqueda | Candidato local conservado |
| --- | --- |
| `resultsOptimo` | `xgboost__w_none` |
| `resultsOptimo_extra_lgbm` | `lightgbm__w_none` |
| `resultsOptimo_extra_lgbm_weights` | `lightgbm__w_cuberoot` |

Se preservan todos los `final_refit`, los estados del ganador, modelos finales, configuraciones, tablas de candidatos, métricas, predicciones y logs. Los checkpoints de L1 principal, L2 y la variante GPU del job 2625 no se podan. La tabla final de `resultsOptimo` no presenta un candidato ExtraTrees exitoso; no se atribuye a esos pesos un score que la evidencia no contiene. Los resúmenes y hashes de las tablas de selección se conservan en [seleccion_y_limpieza_S13.json](seleccion_y_limpieza_S13.json).

## Copias exactas consolidadas

Se consolidaron **8 ocurrencias duplicadas**, que suman **264.731.327 bytes**. Dos son documentos idénticos que coincidían en el destino; las otras seis son archivos pesados idénticos por SHA-256. El [registro de duplicados](duplicados_fusionados.csv) conserva cada origen y la ruta de la única copia física correspondiente. Una coincidencia de tamaño, nombre o CRC sin SHA-256 no se usó para fusionar archivos.

La captura S01 de Slurm queda íntegra, incluidos los mensajes de error repetidos por job. Esos pequeños archivos documentan qué recuperación falló en cada ejecución y forman parte de sus manifiestos. Su repetición no se interpreta como material sobrante.

## Resultado y alcance de verificación

El inventario registra **1.972 ocurrencias de fuente**: 1.969 archivos de los ZIP, el Excel independiente y los dos documentos rectores. Quedan **1.798 archivos originales físicos**, con **4.904.750.553 bytes**. A estos se agrega la documentación derivada de organización y auditoría.

El contenido original destinado a Git ocupa **223.255.900 bytes**. Los **4.681.494.653 bytes** restantes están en `90_artefactos_pesados`, excluido de Git. El umbral de 20 MiB por archivo es una decisión de organización; todos los modelos serializados y la bibliografía de consulta también quedan en ese espejo externo.

Todas las entradas ZIP se descomprimieron comprobando CRC y calculando SHA-256. Los pesos grandes descartados se descomprimieron en flujo para registrar su hash sin conservar otra copia. La verificación final de los archivos físicos retenidos está en `07_reproducibilidad/verificacion_integridad_local.json`. La comprobación remota de Drive registra rutas y tamaños; su alcance no debe confundirse con comparar el SHA-256 de todos los contenidos descargados nuevamente.

El archivo permite rastrear y comprobar la evidencia disponible. No se reentrenaron modelos. Los brutos de CSIC, TorpEda y DS-Augmented-v2 y dos scripts preliminares referenciados no aparecieron en los paquetes; su ausencia queda detallada en las guías de datasets y reproducibilidad.
