import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

# ----------------------------------
# Job setup
# ----------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ----------------------------------
# Data Quality Rules
# ----------------------------------
DEFAULT_DATA_QUALITY_RULESET = """
Rules = [
    ColumnCount > 0
]
"""

# ----------------------------------
# Read from Glue Catalog (S3 Raw)
# ----------------------------------
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="retail_db_catalog",
    table_name="raw",
    transformation_ctx="raw_dyf"
)

# ----------------------------------
# Convert to DataFrame for cleaning
# ----------------------------------
df = raw_dyf.toDF()

# ----------------------------------
# 1. Drop duplicates
# ----------------------------------
df = df.dropDuplicates()

# ----------------------------------
# 2. Basic data validation / filtering
# (example rules – điều chỉnh theo schema thực tế)
# ----------------------------------
if "person_age" in df.columns:
    df = df.filter((F.col("person_age") > 0) & (F.col("person_age") < 100))

if "person_income" in df.columns:
    df = df.filter(F.col("person_income") > 0)

# ----------------------------------
# 3. Handle missing values
# ----------------------------------
fill_defaults = {}

if "loan_int_rate" in df.columns:
    fill_defaults["loan_int_rate"] = 0.0

if "loan_amnt" in df.columns:
    fill_defaults["loan_amnt"] = 0

if fill_defaults:
    df = df.fillna(fill_defaults)

# ----------------------------------
# 4. Normalize categorical values
# ----------------------------------
if "loan_status" in df.columns:
    df = df.withColumn(
        "loan_status",
        F.upper(F.trim(F.col("loan_status")))
    )

# ----------------------------------
# Convert back to DynamicFrame
# ----------------------------------
clean_dyf = DynamicFrame.fromDF(df, glueContext, "clean_dyf")

# ----------------------------------
# Data Quality Check
# ----------------------------------
EvaluateDataQuality().process_rows(
    frame=clean_dyf,
    ruleset=DEFAULT_DATA_QUALITY_RULESET,
    publishing_options={
        "dataQualityEvaluationContext": "dq_check",
        "enableDataQualityResultsPublishing": True
    },
    additional_options={
        "dataQualityResultsPublishing.strategy": "BEST_EFFORT",
        "observations.scope": "ALL"
    }
)

# ----------------------------------
# Optimize output files
# ----------------------------------
if clean_dyf.count() >= 1:
    clean_dyf = clean_dyf.coalesce(1)

# ----------------------------------
# Write to S3 Clean Zone
# ----------------------------------
glueContext.write_dynamic_frame.from_options(
    frame=clean_dyf,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": "s3://retail-data-pipeline-01/clean/"
    }
)

# ----------------------------------
# Write to Amazon RDS (MySQL)
# ----------------------------------
try:
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame=clean_dyf,
        catalog_connection="rds-retail-conn",
        connection_options={
            "database": "retail_db",
            "dbtable": "credit_risk_clean"
        }
    )
except Exception as e:
    print(f"Lỗi ghi vào RDS: {e}")
    raise e

job.commit()
