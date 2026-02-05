# Online Retail Data Pipeline (AWS ETL Project)

## Project Description

This project implements an **end-to-end ETL data pipeline on AWS** using the Online Retail dataset. The pipeline ingests raw CSV data from Amazon S3, processes and cleans it with AWS Glue, and loads the transformed data into Amazon RDS (MySQL/PostgreSQL) for querying and analysis.

The project demonstrates practical skills in cloud-based data ingestion, schema discovery, data transformation, and relational database integration.

---

## Architecture



---

## Implementation Steps

### 1. Store Raw Data on S3

* Create an S3 bucket (e.g. `retail-data-pipeline`)
* Upload `Online Retail.csv` to the `raw/` folder
* (Optional) Create `clean/` folder for processed output

### 2. Create Target Database on RDS

* Create an RDS instance (MySQL or PostgreSQL, Free Tier)
* Configure database credentials
* Enable inbound access on port `3306` (MySQL) or `5432` (PostgreSQL)

### 3. Configure IAM Role & Glue Connection

* Create an IAM role for AWS Glue with access to S3, Glue, and CloudWatch
* Create a Glue JDBC connection to the RDS instance

### 4. Create Glue Data Catalog (Crawler)

* Run a Glue Crawler on `s3://.../raw/`
* Automatically detect the CSV schema
* Store metadata in the Glue Data Catalog

### 5. Build Glue ETL Job

* Use Glue Visual ETL
* Source: Glue Data Catalog table
* Transformations:
  * Remove invalid or duplicate records (optional) ... 
* Target: Amazon RDS
* Automatically create the target table

### 6. Validate Loaded Data

* Connect to RDS using MySQL Workbench



---

## Key Learnings

* Designing a cloud-based ETL pipeline
* Using AWS Glue Crawlers vs ETL Jobs
* Performing schema transformation and data cleaning
* Loading analytical data into Amazon RDS

---

## Author

Nguyễn Văn Toàn
