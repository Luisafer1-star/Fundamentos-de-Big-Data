from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, avg
import time

# 1. Configuración inicial
spark = SparkSession.builder.appName("Analisis Final").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 2. Procesamiento de datos
raw_df = spark.read.text("hdfs:///user/datos/clientes.csv")
header = raw_df.first()[0]
data_df = raw_df.filter(col("value") != header)
split_col = split(col("value"), ";")

df = data_df.select(
    split_col.getItem(0).alias("age"),
    split_col.getItem(1).alias("job"),
    split_col.getItem(2).alias("marital"),
    split_col.getItem(11).cast("float").alias("duration"),
    split_col.getItem(16).alias("y")
)

# 3. Impresión del Reporte
print("\n" + "="*40)
print("--- REPORTE DE ANALISIS DE DATOS ---")
print("="*40)

exitosas_df = df.filter(col("y").contains("yes"))
print(f"\nTotal de llamadas exitosas: {exitosas_df.count()}")

print("\nConteo por edad (Top 5):")
df.groupBy("age").count().orderBy("count", ascending=False).show(5)

print("\nDistribución por estado civil:")
df.groupBy("marital").count().show()

# 4. Cálculo de Promedios
print("\n" + "-"*30)
# Calculamos promedios
res_exito = exitosas_df.select(avg("duration")).collect()[0][0]
prom_exito = res_exito if res_exito is not None else 0
print(f"Duración promedio EXITOSAS: {prom_exito:.2f}")

no_exitosas_df = df.filter(col("y").contains("no"))
res_no_exito = no_exitosas_df.select(avg("duration")).collect()[0][0]
prom_no_exito = res_no_exito if res_no_exito is not None else 0
print(f"Duración promedio NO EXITOSAS: {prom_no_exito:.2f}")
print("-"*30 + "\n")

# 5. BLOQUE DE ESPERA INFINITA (Para la Web UI)
print("="*50)
print("ABRE YA: http://localhost:4040")
print("Tienes 10 segundos antes de que empiece el procesamiento...")
print("="*50)

import time
time.sleep(10)  # TIEMPO PARA ABRIR NAVEGADOR

print("\nIniciando procesamiento para monitoreo...\n")

# Generar jobs LENTOS 
for i in range(5):
    print(f"Ejecutando job pesado {i+1}...")

    df.groupBy("job").count().orderBy("count").show(50)

    time.sleep(3)

print("\nProcesamiento terminado. Manteniendo Spark activo 60 segundos...")
time.sleep(60)  # tiempo para explorar la UI

spark.stop()
