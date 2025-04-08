**Data Classification Table
|Column Name        |Dataset        |Clasification      |Note                              |
|-------------------|---------------|-------------------|----------------------------------|
|CustomerID         |e-commerce	    |Confidential (PII) |Should be marked in future outputs|
|Email	            |e-commerce	    |Confidential (PII)	|Should be encrypted in storage    |
|Description	    |e-commerce	    |Public 	        |No protection needed              |
|XXX	            |XXX	        |XXX	            |XXXX                              |

---

**Data Retention & Archival Policy
    - **How long will you keep raw, processed, or sensitive data?
        - **Raw data will be kept for
        - **Processed data will be kept for
        - **Sensitive data will be kept for

    - **When and how will you archive or delete old data?
        - **Raw data will be
        - **Processed data will be
        - **Sensitive data will be

    - **Where will archived data be stored (e.g., MinIO, external drive)?
        - **Raw data will be kept in
        - **Processed data will be kept in
        - **Sensitive data will be kept in

---

**Audit & Monitoring Strategy
    - **How will we monitor and track Data access
        - 

    - **How will we monitor and track changes made to data or pipeline configurations
        - 

---

**Define Access Control (RBAC)
|Role           |Access Description                     |
|---------------|---------------------------------------|
|Data Analyst   |Read-only access to masked/clean data  |
|Data Steward	|Full access to raw and sensitive data  |
|Admin	        |Full control over all pipeline systems |