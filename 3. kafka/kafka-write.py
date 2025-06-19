#!/usr/bin/env python3

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import to_json, col, struct
from datetime import datetime

def main():
   spark = SparkSession.builder.appName("dataproc-kafka-write-app").getOrCreate()

   df = spark.createDataFrame([
      Row(msg=f'{datetime.now()}')
   ])
   df = df.select(to_json(struct([col(c).alias(c) for c in df.columns])).alias('value'))
   df.write.format("kafka") \
      .option("kafka.bootstrap.servers", "rc1b-f8cttd70kuasp8oq.mdb.yandexcloud.net:9091") \
      .option("topic", "dataproc-kafka-topic") \
      .option("kafka.security.protocol", "SASL_SSL") \
      .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
      .option("kafka.sasl.jaas.config",
              "org.apache.kafka.common.security.scram.ScramLoginModule required "
              "username=user1 "
              "password=password1 "
              ";") \
      .save()

if __name__ == "__main__":
    for i in range(100):
      main()