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
1. todo

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
