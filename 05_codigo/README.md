# Código conservado

`base_binaria_historica/waf-ml-starter` conserva la estructura de módulos de la base histórica S05. `pipelines` reúne los scripts Python y lanzadores S11. La captura S01 mantiene otra copia del estado del proyecto en `02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias`.

Los archivos originales conservan sus nombres y bytes. No se fusionan automáticamente las versiones distintas de `http_features.py`, `ocsvmOptimo.py`, `build_features_csic.py` o `requirements.txt`. La [comparación de versiones](../02_auditoria/historial_slurm/variantes_codigo.csv) identifica cuáles coinciden y cuáles difieren.

La asociación entre etapa y script se registra en el inventario. Una coincidencia de nombre no demuestra qué bytes ejecutó un job antiguo: la [revisión Slurm](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) distingue configuraciones, nombres candidatos y hashes realmente anclados en logs o en el libro.

Los scripts históricos contienen rutas, recursos y parámetros del entorno original. Antes de lanzar una ejecución nueva hay que preparar su entorno y entradas conforme a la configuración de la corrida. La carpeta de [reproducibilidad](../07_reproducibilidad/README.md) permite verificar el archivo y los resultados conservados sin ejecutar entrenamientos.
