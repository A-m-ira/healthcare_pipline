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
