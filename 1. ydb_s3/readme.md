1. Данные сгенерированы скриптом generate_transactions_dataset.py
2. В YDB создана таблица командой: \
  ydb -e grpcs://lb.etnj****.ydb.mdb.yandexcloud.net:2135 \\ \
  -d /ru-central1/b1g6****/etnj**** \\ \
  --iam-token-file iam-token.txt \\ \
  yql -s \\ \
  "create table dataset ( \
    TransactionID Uint64, \
   UserID Uint64, \
   TransactionDate Date, \
   Category String, \
   Product String, \
   Quantity Uint32, \
   PricePerUnit Double, \
   TotalPrice Double, \
   primary key (TransactionID) \
   );"
3. Данные загружены командой: \
  ydb \\ \
   --endpoint grpcs://lb.etnj****.ydb.mdb.yandexcloud.net:2135 \\ \
   --database /ru-central1/b1g6****/etnj**** \\ \
   --iam-token-file iam-token.txt \\ \
  import file csv -p dataset transactions_dataset.csv --header
4. Результат можно увидеть в папке screenshots файл ydb.png
5. В Data Transfer был создан трансфер из ydb в s3: в папке screenshots файл transfer.png
6. Результат трансфера можно увидеть в папке screenshots файл s3.png
