# Group6 Data Transformation and Analytics (DTA) Project

## Team Members
- William Mayer
- Chariya Chhay
- Josh Nyamsi

## 🎯 Project Overview

This project implements a complete data engineering pipeline for processing, transforming, and visualizing data from multiple sources (CSV, JSON, PDF). The system leverages industry-standard tools to automate data ingestion, transformation, storage, and visualization.

### Key Features

- **Automated Data Ingestion**: Process and clean data from various formats (CSV, JSON, PDF)
- **Data Transformation**: ETL pipeline for structuring and enriching data
- **Data Storage**: Both relational (PostgreSQL) and object storage (MinIO)
- **Orchestration**: Workflow management with Apache Airflow
- **Visualization**: Interactive dashboards with Apache Superset or pgAdmin
- **Containerization**: Reproducible environment with Docker

## 📊 Data Sources

This project processes the following datasets:

1. **E-Commerce Sales Transactions** (CSV)
   - Source: UCI Machine Learning Repository
   - Transformation: Data cleaning, normalization, and loading into PostgreSQL

2. **Customer Reviews & Feedback** (JSON)
   - Source: Yelp Academic Json Files
   - Transformation: Text extraction, sentiment analysis, and structuring into tables

3. **Annual Financial Reports** (PDF)
   - Source: Sample Financial Statements
   - Transformation: Conversion to structured format and storage in object storage

## 🏗️ Architecture

The system consists of the following components:

```
┌─────────────────┐     ┌────────────────┐     ┌─────────────────┐
│   Data Sources  │────>│  Data Ingestion │────>│   MinIO         │
│   CSV/JSON/PDF  │     │  (Python)       │     │   (Object Store)│
└─────────────────┘     └────────────────┘     └────────┬────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌────────────────┐     ┌─────────────────┐
│   Visualization │<────│  Transformation │<────│   PostgreSQL    │
│   (Superset)    │     │  (Airflow DAGs) │     │   (Database)    │
└─────────────────┘     └────────────────┘     └─────────────────┘
```

- **Docker Containers**: All components run in containers for easy deployment
- **PostgreSQL**: Relational database for structured data storage
- **MinIO**: S3-compatible object storage for raw and processed files
- **Airflow**: Workflow orchestration for ETL processes
- **Superset/pgAdmin**: Data visualization and exploration

## 🚀 Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Git
- 4GB+ RAM available for containers

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Group6_DTA_Final_Project.git
   cd Group6_DTA_Final_Project
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Wait for all services to initialize (this may take a few minutes)

4. Access the interfaces:
   - Airflow: http://localhost:8080 (username: admin1, password: admin123)
   - MinIO: http://localhost:9001 (username: minioadmin, password: minioadmin)
   - Superset: http://localhost:8088 (username: admin, password: admin)
   - pgAdmin: http://localhost:5050 (email: admin@pgadmin.com, password: admin)

### Initial Configuration

1. Create the required database tables:
   ```bash
   docker-compose exec postgres psql -U airflow -d airflow -f /iceberg-tables/create_tables.sql
   ```

2. Place your datasets in the `data` directory:
   - CSV files for e-commerce transactions
   - JSON files for customer reviews
   - PDF files for financial reports

3. Run the data ingestion script:
   ```bash
   docker-compose exec airflow python /opt/airflow/scripts/ingest_data.py
   ```

4. In the Airflow UI, enable and trigger the `elt_pipeline` DAG

## 📋 Usage Instructions

### Data Ingestion

The `ingest_data.py` script automatically processes all supported file types in the `data` directory:

- For CSV files: Cleans and standardizes data, then uploads to MinIO
- For JSON files: Extracts relevant fields, performs sentiment analysis, and uploads to MinIO
- For PDF files: Extracts text content, identifies key financial metrics, and stores structured data in MinIO

### Data Transformation

The Airflow DAG (`elt_pipeline.py`) orchestrates the following processes:

1. Runs data ingestion to process new files
2. Loads processed data from MinIO into PostgreSQL tables
3. Creates analytics views for easy reporting
4. Performs additional transformations as needed