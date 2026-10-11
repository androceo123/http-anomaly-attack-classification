# Código y lanzadores Slurm

Esta carpeta contiene las implementaciones y los lanzadores conservados de los experimentos HTTP en Arandu. La [guía del entorno Slurm](../07_reproducibilidad/ENTORNO_SLURM.md) explica la preparación de datos, los recursos, las variables de entorno y los comandos de comprobación y envío.

| Ubicación | Función |
| --- | --- |
| [base_binaria_historica/waf-ml-starter](base_binaria_historica/waf-ml-starter) | Módulos de carga, extracción de atributos y entrenamiento de la base binaria, junto a sus lanzadores `jobs/`. |
| [pipelines](pipelines) | Implementaciones y lanzadores de multiclase, multietiqueta y antecedentes one-class. |
| [Captura del proyecto en Arandu](../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias) | Estado de código y configuración registrado durante la captura del 03/08/2026; incluye utilidades de auditoría y preparación. |

## Elegir la implementación

El [índice de experimentos](../04_experimentos/README.md) relaciona las etapas con su evidencia. L2 utiliza `multietiquetaCorrida2.py` y su lanzador; el modelo multiclase fixed30 utiliza `train_waf_multiclass_DEFINITIVO_histgb_fixed30.py`; la extensión de 73 atributos utiliza `3datasetsMulticlase3.py`.

Las variantes mantienen sus nombres y bytes. La [comparación de versiones](../02_auditoria/historial_slurm/variantes_codigo.csv) distingue copias iguales y diferentes de los módulos. La [revisión Slurm](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) indica el grado de evidencia de cada relación entre código, trabajo y resultados.

## Preparación de una nueva corrida

Descargar los datos mediante las [fuentes públicas](../03_datasets/README.md) y preparar las rutas esperadas por el lanzador elegido. Las rutas históricas de los scripts corresponden al proyecto en el clúster; los ejemplos de la guía permiten configurar un directorio de trabajo y salidas propios sin cambiar el código experimental conservado.

Las variables de configuración dependen del lanzador. Varios aceptan `PROJECT_DIR`, `TRAIN_PY` y `CHECK_ONLY`; `run_csic_oneclass_gpu_optimo.sh` utiliza `PY_SCRIPT` y no implementa esa comprobación previa. `3datasetsMulticlase3.sh` fija el Python dentro de `PROJECT_DIR` y valida su SHA-256. Consultar cada caso en la guía antes del envío.

## Componentes históricos con requisitos adicionales

| Componente | Situación documentada |
| --- | --- |
| Lanzador TorpEda preliminar v10 | El nombre exacto `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` no está publicado en esta revisión. |
| Lanzador multietiqueta preliminar multifamily | Su nombre Python predeterminado incluye `DEFINITIVO`; la variante conservada tiene otro nombre. La equivalencia de versiones debe verificarse. |
| Lanzadores `run_resume_multilabel_xgb_cpu_c2.sh` y `c3.sh` | El nombre CPU no determina el backend. Para CPU se debe configurar explícitamente `USE_GPU=off`, como documenta el job3151. |
| Quickstart de la base binaria histórica | Hace referencia a `waf_ml.scripts.train_ocsvm` y `waf_ml.waf.proxy`, módulos ausentes. Los puntos de entrada publicados se consultan en `src/waf_ml/scripts` y `jobs`. |
| Dependencias | Los requisitos y los inventarios de paquetes pertenecen a momentos distintos. La guía muestra esas diferencias y las versiones observadas. |

Una ejecución nueva debe conservar su propio identificador de job, código, hashes de datos, configuración y resultados. Los scripts y registros históricos permiten revisar el trabajo realizado; las comprobaciones de integridad y de métricas están en [reproducibilidad](../07_reproducibilidad/README.md).
