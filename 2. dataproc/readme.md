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
