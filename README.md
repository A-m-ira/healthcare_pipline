# Healthcare Data Pipeline

A complete Healthcare Data Engineering Pipeline project built using modern data engineering tools and workflows. This project demonstrates how healthcare data can be ingested, transformed, orchestrated, and loaded into a cloud data warehouse for analytics and reporting.

---

#  Project Overview

This pipeline demonstrates a complete modern Data Engineering workflow including:

- Real-time data simulation
- Distributed data processing with Spark
- Data Lake architecture using HDFS
- ETL transformations
- Star Schema modeling
- Workflow orchestration using Airflow
- Cloud Data Warehouse loading using Snowflake

---

#  Architecture

```text
CSV Dataset
     ↓
Data Simulator
     ↓
Landing Zone (JSON)
     ↓
Spark Extract Job
     ↓
HDFS Bronze Layer
     ↓
Spark Transformation Job
     ↓
Gold Layer (Star Schema)
     ↓
Snowflake Data Warehouse
```
---

# Technologies Used
### Python
PySpark
Hadoop HDFS
Apache Airflow
YARN
Docker
Snowflake
Parquet
Star Schema
---

# Storage Layers

## Bronze Layer

Raw ingested healthcare data stored in HDFS as Parquet files.

### Path

```bash
hdfs://hadoop-namenode:9000/user/jovyan/bronze/healthcare/
```

---

## Gold Layer

Curated and transformed analytical data stored in Star Schema format.

### Path

```bash
hdfs://hadoop-namenode:9000/user/root/datalake/gold/
```

---

#  Example Snowflake Queries

##  View Patient Data

```sql
SELECT * 
FROM DIM_PATIENT
LIMIT 10;
```

---

##  View Fact Table

```sql
SELECT * 
FROM FACT_HEALTHCARE
LIMIT 10;
```

---

##  Count Total Records

```sql
SELECT COUNT(*) 
FROM FACT_HEALTHCARE;
```

---

##  Example Analytical Query

```sql
SELECT
    d.AGE,
    d.GENDER,
    f."BILLING AMOUNT"
FROM FACT_HEALTHCARE f
JOIN DIM_PATIENT d
ON f.PATIENT_KEY = d.PATIENT_KEY;
```
