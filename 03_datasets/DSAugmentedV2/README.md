# DS-Augmented-v2 / egipcios

Este corpus aparece en el código y los resultados con el alias `egipcios`. Los nombres se conservan en las rutas históricas; el [catálogo de datasets](../README.md) unifica su identificación documental.

## Universo, clases y disponibilidad

Los artefactos comparados de M7/M8 contienen **704.665 registros**, repartidos en 563.732 de desarrollo y 140.933 de prueba. En esas etapas se utiliza una taxonomía canónica de ocho clases. La extensión de 73 atributos conserva nueve clases nativas; ambas formulaciones quedan identificadas por separado.

En los trece ZIP **no se encontró una copia de la fuente cruda**. Se conservan las matrices procesadas y los artefactos experimentales disponibles. El [catálogo externo](../../07_reproducibilidad/artefactos_externos.csv) registra los archivos grandes, sus hashes y su ubicación en Drive.

## Corridas y auditoría

- [M7: tres corpus y 58 atributos](../../04_experimentos/multiclase/M7_tres_corpus_58/README.md).
- [M8: tres corpus y 72 atributos](../../04_experimentos/multiclase/M8_tres_corpus_72/README.md).
- [EXP73: extensión de 73 atributos](../../04_experimentos/extensiones/EXP_73_atributos/README.md). Se conserva como extensión y no se presenta como una etapa M9 del libro.
- [Revisión de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md): reconciliación de atributos, universos, clases y métricas.

Las curvas de M8 para este corpus se generaron sobre una muestra de 50.000 registros; las métricas globales corresponden al conjunto de prueba de 140.933. Esta diferencia de soporte está documentada para que los gráficos no se interpreten como una nueva partición completa.

## Organización de los procesados

Las matrices de 58, 72 y 73 atributos permanecen asociadas a M7, M8 y EXP73, respectivamente. No se intercambian por compartir el mismo alias de corpus. El [inventario de procedencia](../../02_auditoria/integridad_y_procedencia/inventario_archivos.csv) relaciona cada ruta organizada con su fuente original y SHA-256. Consulte la [guía de reproducibilidad](../../07_reproducibilidad/README.md) antes de adaptar una ejecución nueva.
