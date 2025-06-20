import uuid
import datetime
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.yandex.operators.yandexcloud_dataproc import (
    DataprocCreateClusterOperator,
    DataprocCreatePysparkJobOperator,
    DataprocDeleteClusterOperator,
)

# Данные вашей инфраструктуры
YC_DP_AZ = 'ru-central1-b'
YC_DP_SSH_PUBLIC_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDZrPimmkDeEdwzxwPDx5t9mdjM4DiG6302vnPJULLsM3c5YZjrdKI/7S+h6i6P5TDiSW872p70ue5cag+1XfqScLS6yqg79t1VE5N8jO9CA/X29Dp8Jqr7efxWRz9kjU7rcJ3UscA353vxUyweQ5NguOzXDDpeYLF7gZDt/ZS5Kg/jBq2+N8WvAMRMJ6CbUb4Bv5KTEOWu8x5tZZa/QtJu2UWqUXinHWVGO/QpAAE1gc6pg4WxVyLtUT+zyEyTYT+V0bZCMPUKyR4W/F0ixaowe8yr4FDnpPtPLCluPbCumgJ7nalq15H0xJ3Xm3edSzlqFLt1fxiguyjcK9ndn/ShkqFTdvmaw5JFcvEb1/30DfrrIwT90Mkc7Hz/K35bY9+FLz9HzcaYn/e+uc3gaK2isL6nIryiigt7i1bCocPU6TwnbNTioidcdJLnhLD7/DoRv3SGbtUo1H3mEyJrmjejy/QVmkzjY9AkE1doXGQiRg9nSeGHgEIB2UKwtfk2H8= marja@MacBook-Pro-Marja.local'
YC_DP_SUBNET_ID = 'e2ldsshln0568dsoukc1'
YC_DP_SA_ID = 'aje0tnshsp5926t9ti6u'
YC_DP_METASTORE_URI = '172.16.0.7'
YC_BUCKET = 'elt-airflow'

# Настройки DAG
with DAG(
        'DATA_INGEST',
        schedule_interval='@hourly',
        tags=['data-processing-and-airflow'],
        start_date=datetime.datetime.now(),
        max_active_runs=1,
        catchup=False
) as ingest_dag:
    # 1 этап: создание кластера Yandex Data Proc
    create_spark_cluster = DataprocCreateClusterOperator(
        task_id='dp-cluster-create-task',
        cluster_name=f'tmp-dp-{uuid.uuid4()}',
        cluster_description='Временный кластер для выполнения PySpark-задания под оркестрацией Managed Service for Apache Airflow™',
        ssh_public_keys=YC_DP_SSH_PUBLIC_KEY,
        service_account_id=YC_DP_SA_ID,
        subnet_id=YC_DP_SUBNET_ID,
        s3_bucket=YC_BUCKET,
        zone=YC_DP_AZ,
        cluster_image_version='2.1',
        masternode_resource_preset='s2.small',
        masternode_disk_type='network-ssd',
        masternode_disk_size=32,
        computenode_resource_preset='s2.small',
        computenode_disk_type='network-ssd',
        computenode_disk_size=32,
        computenode_count=1,
        computenode_max_hosts_count=2,  # Количество подкластеров для обработки данных будет автоматически масштабироваться в случае большой нагрузки.
        services=['YARN', 'SPARK'],     # Создается легковесный кластер.
        datanode_count=0,               # Без подкластеров для хранения данных.
        properties={                    # С указанием на удаленный кластер Metastore.
            'spark:spark.hive.metastore.uris': f'thrift://{YC_DP_METASTORE_URI}:9083',
        },
    )

    # 2 этап: запуск задания PySpark
    poke_spark_processing = DataprocCreatePysparkJobOperator(
        task_id='dp-cluster-pyspark-task',
        main_python_file_uri=f's3a://{YC_BUCKET}/in/analyse.py',
    )

    # 3 этап: удаление кластера Yandex Data Processing
    delete_spark_cluster = DataprocDeleteClusterOperator(
        task_id='dp-cluster-delete-task',
        trigger_rule=TriggerRule.ALL_DONE,
    )

    # Формирование DAG из указанных выше этапов
    create_spark_cluster >> poke_spark_processing >> delete_spark_cluster
