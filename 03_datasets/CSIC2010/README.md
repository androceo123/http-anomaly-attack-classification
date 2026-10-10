# CSIC2010

CSIC2010 participa en el desarrollo binario y en los antecedentes de detección de anomalías. Esta carpeta es el punto de entrada al corpus; los resultados y configuraciones permanecen junto a cada corrida.

## Disponibilidad

En los trece ZIP examinados **no se encontró una copia de la fuente cruda de CSIC2010**. Se conservan código, informes y artefactos derivados. Los archivos externos disponibles se identifican en el [catálogo](../../07_reproducibilidad/artefactos_externos.csv); la ausencia del original impide afirmar que el archivo entregado permite repetir por sí solo toda la preparación desde cero.

El [catálogo de datasets](../README.md) describe el esquema común y la relación entre los corpus. Los nombres y rutas históricas del código se conservan literalmente y requieren adaptación al entorno de una ejecución nueva.

## Corridas y análisis

- [B1: ablación de atributos](../../04_experimentos/binario/B1_ablacion_csic/README.md): comparación documentada de conjuntos de 25, 33, 57 y 10 atributos. El alias histórico RF34 corresponde a 33 atributos; no debe confundirse con el conjunto de 34 de OCSVM.
- [B2: comparación de corpus](../../04_experimentos/binario/B2_comparacion_corpus/README.md): entrenamientos Random Forest independientes por corpus. El nombre original `cross_dataset` no demuestra transferencia de un modelo entre datasets.
- [Antecedente one-class](../../04_experimentos/antecedentes/oneclass_csic/README.md): salidas históricas de la detección de anomalías.
- [Revisión de Slurm y del desarrollo binario](../../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md): vínculo entre código, informes, jobs y diferencias de versiones.

## Procedencia y alcance

El [inventario de procedencia](../../02_auditoria/integridad_y_procedencia/inventario_archivos.csv) registra los archivos conservados con sus nombres originales y hashes. Las etapas binarias mantienen el carácter exploratorio explicado por la tesis, incluida la consulta al conjunto de prueba durante el desarrollo. Una nueva ejecución debe conservar otra identidad de corrida y sus propias entradas, particiones y entorno.
