# TorpEda2012

Los artefactos usan los alias `TorpEda`, `TorpEda2012` y `torpeda`. Las matrices procesadas y sus resultados permanecen junto a cada corrida, para conservar la versión de atributos y taxonomía empleada.

## Universo y disponibilidad

En los artefactos comparados de M7/M8, el corpus contiene **74.133 registros**, con 59.306 para desarrollo y 14.827 para prueba, y una formulación multiclase de diez clases. El [análisis de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) documenta las fuentes de estos valores y su alcance.

**No se encontró la fuente cruda de TorpEda2012 en los trece ZIP.** Se conservaron los procesados, código, configuraciones, predicciones e informes disponibles. El [catálogo externo](../../07_reproducibilidad/artefactos_externos.csv) permite localizar las matrices y modelos pesados por corrida, tamaño y SHA-256.

## Corridas relacionadas

- [B2: comparación binaria de corpus](../../04_experimentos/binario/B2_comparacion_corpus/README.md): modelo independiente por corpus.
- [M1: fixed30](../../04_experimentos/multiclase/M1_fixed30/README.md): primera etapa multiclase documentada.
- [M7: tres corpus y 58 atributos](../../04_experimentos/multiclase/M7_tres_corpus_58/README.md).
- [M8: tres corpus y 72 atributos](../../04_experimentos/multiclase/M8_tres_corpus_72/README.md).
- [Extensión de 73 atributos](../../04_experimentos/extensiones/EXP_73_atributos/README.md): evidencia posterior al alcance principal del libro y la presentación.

En M8, las curvas de TorpEda utilizan el conjunto de prueba de 14.827 registros. La situación difiere de las curvas de Harvard y DS-Augmented, que se produjeron sobre muestras de 50.000. Los denominadores de cada artefacto se conservan en la auditoría.

El [inventario](../../02_auditoria/integridad_y_procedencia/inventario_archivos.csv) y el [catálogo de corridas](../../06_resultados_consolidados/catalogo_corridas.csv) permiten seguir cada archivo hasta su paquete original. La comparación de corpus del archivo no constituye por sí misma una evaluación de transferencia entre corpus.
