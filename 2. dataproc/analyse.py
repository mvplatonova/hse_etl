from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, to_date, current_date
from datetime import datetime

spark = SparkSession.builder \
   .appName("transactions-analysis") \
   .enableHiveSupport() \
   .getOrCreate()

sales_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://elt-airflow/in/transactions_dataset.csv")

sales_df = sales_df.withColumn("TransactionDate", to_date(col("TransactionDate")))

daily_sales_summary = sales_df \
    .groupBy("TransactionDate", "Category") \
    .agg(sum("TotalPrice").alias("DailySalesAmount"))

current_date_str = datetime.now().strftime("%Y-%m-%d")
output_path = f"s3a://elt-airflow/out/transactions-analysis_{current_date_str}"

daily_sales_summary.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)
