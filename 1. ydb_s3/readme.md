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
6. Загруженные данные ([result/ydb.png](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/ydb.png)):
![alt text](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/ydb.png =250x)
8. В Data Transfer был создан трансфер из ydb в s3 ([result/transfer.png](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/transfer.png)):
![alt text](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/transfer.png)
10. Успешный результат трансфера представлен в файле [result/dataset.csv](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/dataset.csv) и дополниельно [скриншот](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/s3.png) из s3:
![alt text](https://github.com/mvplatonova/hse_etl/blob/main/1.%20ydb_s3/result/s3.png)
