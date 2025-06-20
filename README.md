# Отчет по итоговому заданию

### 1. Работа с Yandex DataTransfer
1. Данные сгенерированы скриптом generate_transactions_dataset.py
2. В YDB создана таблица командой:
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
4. Данные загружены командой:
```bash
  ydb \
   --endpoint grpcs://lb.etnj****.ydb.mdb.yandexcloud.net:2135 \
   --database /ru-central1/b1g6****/etnj**** \
   --iam-token-file iam-token.txt \
  import file csv -p dataset transactions_dataset.csv --header
```
6. Результат можно увидеть в папке screenshots файл ydb.png
7. В Data Transfer был создан трансфер из ydb в s3: в папке screenshots файл transfer.png
8. Результат трансфера можно увидеть в папке screenshots файл s3.png

### 2. Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow
1. Подготовлена инфраструктура по [инструкции](https://yandex.cloud/ru/docs/managed-airflow/tutorials/data-processing-automation#infra)
    - S3 бакет
    - Metastore кластер
    - Airflow кластер
2. Данные были сгенерированы скриптом из первого задания (сам скрипт и csv файл лежат в папке "1. ydb_s3")
3. PySpark задание (файл analyse.py) считает ежедневную выручку по категориям товаров и записывает данные в s3
4. В файле etl-dag.py находится dag DATA_INGEST, который создает кластер, запускает задание, удаляет кластер
5. В папке result лежит скриншот успешного запуска DAG, а также скриншот и файл полученного результата в s3 

### 3. Работа с топиками Apache Kafka с помощью PySpark заданий в Yandex Data Processing
1. Подготовлена инфраструтура по [инструкции](https://yandex.cloud/ru/docs/managed-kafka/tutorials/data-processing#infra)
    - S3 бакет
    - Data Processing кластер
    - Kafka кластер
    - Kafka топик
    - Kafka пользователь
2. В DataProc создано и запущено задание kafka-write
3. В DataProc создано и запущено задание kafka-stream-read
4. В папке result лежат скриншоты успешных запусков заданий, а также вывод задания чтения
