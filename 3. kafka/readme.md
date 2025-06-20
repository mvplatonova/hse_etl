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

