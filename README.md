# Отчет по итоговому заданию

## 1. Работа с Yandex DataTransfer
1. Данные сгенерированы скриптом [generate_transactions_dataset.py](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/generate_transactions_dataset.py)
2. В YDB создана таблица с помощью команды:
```bash
  ydb -e grpcs://lb.etnj****.ydb.mdb.yandexcloud.net:2135 \
  -d /ru-central1/b1g6****/etnj**** \
  --iam-token-file iam-token.txt \
  yql -s \
  "create table dataset ( 
    TransactionID Uint64, 
   UserID Uint64, 
   TransactionDate Date, 
   Category String, 
   Product String, 
   Quantity Uint32, 
   PricePerUnit Double, 
   TotalPrice Double, 
   primary key (TransactionID) 
   );"
```
4. Данные загружены с помощью команды:
```bash
  ydb \
   --endpoint grpcs://lb.etnj****.ydb.mdb.yandexcloud.net:2135 \
   --database /ru-central1/b1g6****/etnj**** \
   --iam-token-file iam-token.txt \
  import file csv -p dataset transactions_dataset.csv --header
```
6. Загруженные данные в YDB ([result/ydb.png](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/ydb.png)):

<img src="https://raw.githubusercontent.com/mvplatonova/hse_etl/main/1.%20ydb_s3/result/ydb.png" alt="текст" width="750"/>

8. В Data Transfer был создан трансфер из ydb в s3 ([result/transfer.png](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/transfer.png)):

<img src="https://raw.githubusercontent.com/mvplatonova/hse_etl/main/1.%20ydb_s3/result/transfer.png" alt="текст" width="750"/>

10. Успешный результат трансфера представлен в файле [result/dataset.csv](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/dataset.csv) и дополниельно
 [скриншот](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/s3.png) из s3:

<img src="https://raw.githubusercontent.com/mvplatonova/hse_etl/main/1.%20ydb_s3/result/s3.png" alt="текст" width="750"/>

## 2. Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow
1. Подготовлена инфраструктура по [инструкции](https://yandex.cloud/ru/docs/managed-airflow/tutorials/data-processing-automation#infra)
    - S3 бакет
    - Metastore кластер
    - Airflow кластер
2. Данные были сгенерированы скриптом из [первого задания](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/generate_transactions_dataset.py)
3. PySpark задание (файл [analyse.py](https://github.com/mvplatonova/hse_etl/blob/main/2.%20dataproc/analyse.py)) считает ежедневную выручку по категориям товаров и записывает данные в s3
4. В файле [etl-dag.py](https://github.com/mvplatonova/hse_etl/blob/main/2.%20dataproc/etl_dag.py) находится dag DATA_INGEST, который создает кластер, запускает задание, удаляет кластер
5. Успешный запуск dag ([result/airflow.png](https://github.com/mvplatonova/hse_etl/blob/main/2.%20dataproc/result/airflow.png))

<img src="https://raw.githubusercontent.com/mvplatonova/hse_etl/main/2.%20dataproc/result/airflow.png" alt="текст" width="750"/>

6. Результат запука [result/part-00000-9daa6e90-c21b-4623-bdd3-9157a8015380-c000.csv](https://github.com/mvplatonova/hse_etl/blob/main/2.%20dataproc/result/part-00000-9daa6e90-c21b-4623-bdd3-9157a8015380-c000.csv)  и дополниельно [скриншот](https://github.com/mvplatonova/hse_etl/blob/main/2.%20dataproc/result/s3.png) из s3:

<img src="https://raw.githubusercontent.com/mvplatonova/hse_etl/main/2.%20dataproc/result/s3.png" alt="текст" width="750"/>

## 3. Работа с топиками Apache Kafka с помощью PySpark заданий в Yandex Data Processing
1. Подготовлена инфраструтура по [инструкции](https://yandex.cloud/ru/docs/managed-kafka/tutorials/data-processing#infra)
    - S3 бакет
    - Data Processing кластер
    - Kafka кластер
    - Kafka топик
    - Kafka пользователь
2. В DataProc создано и запущено задание [kafka-write](https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/kafka-write.py), циклически записывающее в топик текущее время и дату

<img src="https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/result/write.png" alt="текст" width="750"/>

4. В DataProc создано и запущено задание [kafka-stream-read](https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/kafka-read-stream.py)

<img src="https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/result/read.png" alt="текст" width="750"/>

6. Вывод задания чтения: файлы [part-00000****.txt](https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/result/part-00000-8d389984-98e1-43e7-891d-cee51bf65a24-c000.txt) и [part-00001****.txt](https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/result/part-00001-8d389984-98e1-43e7-891d-cee51bf65a24-c000.txt)

<img src="https://github.com/mvplatonova/hse_etl/blob/main/3.%20kafka/result/s3.png" alt="текст" width="750"/>

