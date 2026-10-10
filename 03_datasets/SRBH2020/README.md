# SRBH2020 / Harvard

Este corpus aparece en los artefactos como `harvard`, `SRBH2020` o SR-BH. La carpeta reúne su punto de entrada documental; los procesados permanecen asociados a la corrida que los produjo.

## Fuente y universos

El CSV original conservado, `data_capec_multilabel.csv`, contiene **907.815 filas y 38 columnas**, con 525.195 eventos normales y 382.620 de ataque según el perfil recalculado. El [perfil del archivo](../../02_auditoria/datasets_y_multiclase/sr_bh_raw_profile.json) deja explícito el universo observado. La cifra de 907.814 citada en la documentación de la fuente no se sustituye silenciosamente por la del archivo recibido.

La selección multiclase Top14 conserva 902.411 eventos y descarta 5.404 de las combinaciones no incluidas. L1 trabaja con eventos; L2 excluye dos peticiones vacías y agrupa los 907.813 eventos restantes en **542.990 huellas** de quince campos HTTP. Por eso sus denominadores no deben intercambiarse.

El original está en `90_artefactos_pesados/03_datasets/SRBH2020/original/`. El [catálogo externo](../../07_reproducibilidad/artefactos_externos.csv) identifica su ruta, tamaño, SHA-256 y ubicación en Drive.

## Análisis y auditoría

- [Revisión de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md): universos, taxonomías y cambios de las etapas M1–M8.
- [Auditoría recalculada de la planilla](../../02_auditoria/datasets_y_multiclase/S10_auditoria_excel_recalculado.json): repeticiones y conflictos de etiquetas.
- [Evidencia multietiqueta](../../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md): huellas, particiones, reconstrucciones y relación entre predicciones y métricas.
- [Huella de quince campos](../esquemas/huella_peticion_15_campos.json): definición documentada, distinta de comparar todos los campos del evento.

## Corridas relacionadas

El [historial experimental](../../04_experimentos/README.md) recorre las variantes multiclase. [L1](../../04_experimentos/multietiqueta/L1_fixed30/README.md) conserva la etapa fixed30 y su antecedente GPU/job2625 por separado. [L2](../../04_experimentos/multietiqueta/L2_request90/README.md) conserva request90, la agregación por huella y los bloques de entrenamiento, tuning, calibración y prueba.

Las matrices de cada etapa permanecen en sus respectivas corridas; una copia pesada idéntica puede tener una ubicación física compartida. El [inventario](../../02_auditoria/integridad_y_procedencia/inventario_archivos.csv) registra cada origen y su destino canónico. Las reconstrucciones fechadas en octubre de 2026 se distinguen de los artefactos históricos.
