# 🛒 Online Retail Data Pipeline (AWS ETL Project)

## 📌 Project Overview

This project demonstrates an **end-to-end ETL data pipeline on AWS**, using a real-world **Online Retail dataset**.
The pipeline ingests raw CSV data from Amazon S3, processes and cleans it using AWS Glue, and loads the transformed data into an Amazon RDS database (MySQL or PostgreSQL) for analysis.

This project is designed as a **hands-on data engineering portfolio project**, focusing on cloud-native ETL, schema management, and structured data loading.

---

## 🏗️ Architecture

```
Local CSV
   ↓
Amazon S3 (raw)
   ↓
AWS Glue (Crawler + ETL Job)
   ↓
Amazon RDS (MySQL / PostgreSQL)
```

Optional output:

```
AWS Glue
   ↓
Amazon S3 (clean)
```

---

## 🧰 Tech Stack

* **Amazon S3** – Raw and cleaned data storage
* **AWS Glue** – Data Catalog, Crawlers, ETL Jobs
* **Amazon RDS** – MySQL / PostgreSQL
* **AWS IAM** – Access control and permissions
* **SQL** – Data validation and querying
* **CSV / Parquet** – Data formats

---

## 📂 Project Structure (S3)

```
retail-data-pipeline-xxxx/
├── raw/
│   └── Online Retail.csv
├── scripts/
│   └── Glue ETL scripts (auto-generated)
└── clean/        (optional)
    └── processed output files
```

---

## 🚀 Implementation Steps

### Step 1: Prepare Raw Data on Amazon S3

1. Open **Amazon S3 Console**
2. Create a bucket (e.g. `retail-data-pipeline-xxxx`)
3. Inside the bucket, create folders:

   * `raw/` → upload `Online Retail.csv`
   * `scripts/` → used by AWS Glue
   * `clean/` (optional) → store cleaned data

---

### Step 2: Set Up Amazon RDS (Target Database)

1. Go to **RDS Console → Create database**
2. Choose **MySQL** or **PostgreSQL**
3. Configuration:

   * Template: **Free Tier**
   * DB Identifier: `retail-db`
   * Master username/password: save for later use
4. Connectivity:

   * Public access: **Yes** (for learning/demo purposes)
   * Security Group:

     * Allow inbound traffic on port `3306` (MySQL) or `5432` (PostgreSQL)
     * Source: Your IP address and the same security group (for Glue access)

---

### Step 3: Configure IAM Role & Glue Connection

#### IAM Role

1. Go to **IAM → Roles → Create role**
2. Trusted entity: **AWS Glue**
3. Attach policies:

   * `AWSGlueServiceRole`
   * `AmazonS3FullAccess`
   * `CloudWatchLogsFullAccess`

#### Glue Connection

1. Open **AWS Glue → Connections → Create connection**
2. Choose **JDBC**
3. Provide:

   * JDBC URL of the RDS instance
   * Database username & password
4. This enables Glue to connect to RDS

---

### Step 4: Create Glue Data Catalog (Crawler)

1. Go to **AWS Glue → Crawlers → Create crawler**
2. Data source:

   * `s3://retail-data-pipeline-xxxx/raw/`
3. IAM Role: select the Glue IAM role
4. Output:

   * Create a new database (e.g. `retail_catalog`)
5. Run the crawler

After completion, a table representing the CSV schema will appear in the Glue Data Catalog.

---

### Step 5: Build Glue ETL Job

1. Go to **AWS Glue → ETL Jobs → Visual ETL**
2. **Source**:

   * AWS Glue Data Catalog
   * Database: `retail_catalog`
   * Table: Crawled retail table
3. **Transformations**:

   * Change Schema:

     * `InvoiceDate`: string → timestamp
     * `Quantity`: string → integer
   * Optional:

     * Filter invalid records
     * Drop duplicate rows
4. **Target**:

   * Type: MySQL / PostgreSQL
   * Connection: Glue JDBC connection
   * Database: RDS database
   * Table name: `online_retail_clean`
   * Handling strategy: **Create table in target**
5. Save and run the job

---

### Step 6: Validate Results

#### Verify Data in RDS

Use MySQL Workbench, DBeaver, or AWS Query Editor:

```sql
SELECT *
FROM online_retail_clean
LIMIT 10;
```

#### (Optional) Verify Clean Data on S3

```
s3://retail-data-pipeline-xxxx/clean/
```

---

## ⚠️ Important Notes

* **Networking & VPC**

  * If RDS is in a private subnet, create an **S3 Gateway Endpoint**
  * Ensure AWS Glue runs in the same VPC and subnet as RDS

* **Date Format Handling**

  * The Online Retail dataset uses non-standard date formats
  * Always validate and convert dates during schema transformation

* **Cost Control**

  * Delete RDS instances, Glue jobs, and S3 buckets after practice
  * This project is intended to run within Free Tier limits

---

## 🎯 Learning Outcomes

* Build a production-style AWS ETL pipeline
* Understand Glue Crawlers vs Glue ETL Jobs
* Perform schema transformation and data cleaning
* Load structured data into Amazon RDS
* Gain practical cloud data engineering experience

---

## 🚀 Future Improvements

* Incremental data loading
* Partitioned data storage on S3
* Use Parquet format for performance optimization
* Add AWS Glue Data Quality checks
* Build dashboards using Amazon QuickSight

---

## 📎 Dataset

* Online Retail Dataset (UCI Machine Learning Repository)

---

## 👤 Author

Nguyễn Văn Toàn

Data Informatics | Aspiring Data Analyst / Data Engineer
