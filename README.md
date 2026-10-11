# Detección y clasificación de ataques HTTP en Arandu / Slurm

Repositorio de código, documentación y evidencia experimental de la tesis **Detección y clasificación de ataques en tráfico HTTP mediante enfoques binario, multiclase y multietiqueta**. Los experimentos se ejecutaron en **Arandu**, con trabajos gestionados por **Slurm**. El proyecto reúne los lanzadores, las implementaciones, el historial de trabajos y las auditorías que relacionan los resultados con sus datos, configuraciones y condiciones de ejecución.

La referencia académica es el [libro de tesis](01_documentacion/libro/08282026v4.pdf), acompañado de la [presentación](01_documentacion/presentacion/cambiosAndres.pptx). Los antecedentes one-class, las etapas B1–B2, M1–M8 y L1–L2, y la extensión posterior de 73 atributos tienen identidades diferenciadas.

## Entorno de ejecución

La [guía de Arandu y Slurm](07_reproducibilidad/ENTORNO_SLURM.md) documenta los nodos y particiones observados, los entornos Python, las variables de los lanzadores y ejemplos de envío con `sbatch`. Se apoya en la [captura del clúster del 3 de agosto de 2026](02_auditoria/historial_slurm/evidencia_20260803) y en los [registros de trabajos](02_auditoria/historial_slurm/catalogo_jobs.csv).

Los logs y las configuraciones conservan las rutas del proyecto utilizadas en el clúster, entre ellas `/home_data/aroman/TFG/waf-ml-starter`. Para una nueva ejecución se configuran las rutas, los datos y los recursos del entorno de destino, y se asigna un directorio de resultados propio. La captura de entorno tiene una fecha concreta; la asociación de cada resultado con un job se detalla en la [auditoría de Slurm](02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md).

## Datasets: fuentes públicas

Los corpus se descargan por separado. El repositorio contiene sus esquemas, análisis y referencias; las entradas de entrenamiento se preparan en el almacenamiento del entorno de ejecución.

| Dataset | Fuente para obtener los datos | Preparación y alcance |
| --- | --- | --- |
| HTTP CSIC 2010 | [Archivos originales HTTP en msudol](https://github.com/msudol/Web-Application-Attack-Datasets/tree/master/OriginalDataSets/csic_2010) | [Ficha CSIC2010](03_datasets/CSIC2010/README.md) |
| CSIC 2012 / TorpEda | [Repositorio indicado para TorpEda](https://github.com/DuckDuckBug/cnn_waf/tree/master/data), carpeta [XML `torpeda`](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda) | [Ficha TorpEda2012](03_datasets/TorpEda2012/README.md) |
| SR-BH 2020 / Harvard | [Harvard Dataverse, DOI 10.7910/DVN/OGOIXX](https://doi.org/10.7910/DVN/OGOIXX) | [Ficha SRBH2020](03_datasets/SRBH2020/README.md) |
| WAMM / DS-Augmented-v2 | [Repositorio público de Cyshield](https://github.com/CyShield-Security-R-D/WAMM-Dataset-Repository) | [Ficha DS-Augmented-v2](03_datasets/DSAugmentedV2/README.md) |

Las fichas distinguen el formato público del formato preparado para los scripts. Para comparar una ejecución nueva con una histórica hay que registrar versión, tamaño, hash, etiquetas y transformaciones. Los procesados y modelos de una corrida son resultados del pipeline y tienen una identidad distinta de la fuente descargable del dataset.

## Estructura del proyecto

| Carpeta | Contenido |
| --- | --- |
| [01_documentacion](01_documentacion/README.md) | Libro, presentación, referencias y antecedentes de la tesis. |
| [02_auditoria](02_auditoria/README.md) | Duplicados, conflictos, particiones, evidencia Slurm, identidad de código y límites de los resultados. |
| [03_datasets](03_datasets/README.md) | Fuentes públicas, formatos de entrada, universos, taxonomías CAPEC y esquemas de atributos. |
| [04_experimentos](04_experimentos/README.md) | Índice de etapas, jobs y evidencia disponible. |
| [05_codigo](05_codigo/README.md) | Base binaria, pipelines y lanzadores Slurm. |
| [06_resultados_consolidados](06_resultados_consolidados/README.md) | Catálogo de corridas, configuraciones y métricas registradas. |
| [07_reproducibilidad](07_reproducibilidad/README.md) | Preparación del entorno, integridad del repositorio y comprobación de resultados. |

## Comenzar una reproducción

1. Obtener los datos siguiendo las fichas de [datasets](03_datasets/README.md).
2. Preparar el entorno y elegir un lanzador según la [guía Slurm](07_reproducibilidad/ENTORNO_SLURM.md).
3. Comprobar las entradas, la versión del código y las rutas de salida; utilizar la comprobación previa del lanzador cuando esté disponible.
4. Enviar la nueva corrida mediante `sbatch` y conservar su configuración, logs, semillas, particiones, hashes y contabilidad de Slurm.

Para comprobar los archivos publicados, con Python 3.11 o posterior:

```bash
python 07_reproducibilidad/scripts/verificar_integridad.py --root .
```

La [guía de reproducibilidad](07_reproducibilidad/README.md) separa esta comprobación del recálculo de métricas, que requiere las predicciones y demás artefactos de cada corrida. Los catálogos identifican qué archivos están publicados y cuáles están únicamente referenciados. El índice de experimentos permite navegar la evidencia disponible sin asumir que contiene todas las salidas históricas.

## Auditoría y alcance de los resultados

La auditoría forma parte de la contribución de la tesis. Distingue eventos completos, identidad de petición mediante quince campos HTTP, conflictos de etiquetas y separación efectiva de particiones. También diferencia una configuración vinculada a un job, una coincidencia de nombre de script y una identidad de código acreditada por hash.

Las etapas binarias, multiclase y L1 conservan el alcance exploratorio explicado en el libro. L2 agrupa peticiones y separa entrenamiento, selección, calibración y prueba. Las verificaciones fechadas en octubre de 2026 identifican sus particiones como reconstrucciones; sus resultados no equivalen por sí solos a validación temporal, transferencia entre corpus o rendimiento en producción.

Las metas por clase y etiqueta se consultan junto a las métricas globales. En L2 NORMAL reconoce 33.925 de 34.270 casos (98,9933 %), y CAPEC-153 y CAPEC-272 quedan por debajo de F1 0,85. Los detalles y sus denominadores están en la [guía de auditoría](02_auditoria/README.md) y en la [verificación L2](02_auditoria/particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json).
