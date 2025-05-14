# 📘 Database Connection Guide

This guide explains how to connect to **SQL Server** and **PostgreSQL** databases using Python. It covers both **local** and **cloud (Azure/AWS)** scenarios using `pyodbc` and `psycopg2`.

---

## 📦 Prerequisites

### 🔹 Install Required Packages

```bash
pip install pyodbc psycopg2-binary
```

---

# 🗄️ SQL Server (Using `pyodbc`)

## 1️⃣ Local SQL Server Connection

### 🔹 Case 1: Trusted Connection (Windows Authentication)

```python
import pyodbc

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost\SQLEXPRESS;'
    r'DATABASE=YourDatabaseName;'
    r'Trusted_Connection=yes;'
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
row = cursor.fetchone()
print("Connected to:", row[0])
conn.close()
```

---

### 🔹 Case 2: SQL Authentication (Username & Password)

```python
import pyodbc

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost;'
    r'DATABASE=YourDatabaseName;'
    r'UID=your_username;'
    r'PWD=your_password;'
)

cursor = conn.cursor()
cursor.execute("SELECT DB_NAME()")
row = cursor.fetchone()
print("Connected to database:", row[0])
conn.close()
```

---

## 2️⃣ Azure SQL Database Connection

### 🔹 Case 1: SQL Authentication (Recommended)

```python
import pyodbc

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=your_server_name.database.windows.net;'
    r'DATABASE=YourDatabaseName;'
    r'UID=your_username;'
    r'PWD=your_password;'
    r'Encrypt=yes;'
    r'TrustServerCertificate=no;'
    r'Connection Timeout=30;'
)

cursor = conn.cursor()
cursor.execute("SELECT SUSER_SNAME()")
row = cursor.fetchone()
print("Connected as:", row[0])
conn.close()
```

---

### 🔹 Case 2: Azure AD Integrated Authentication

> ⚠️ Requires Azure Active Directory configuration and domain-joined machine.

```python
import pyodbc

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=your_server_name.database.windows.net;'
    r'DATABASE=YourDatabaseName;'
    r'Authentication=ActiveDirectoryIntegrated;'
    r'Encrypt=yes;'
    r'TrustServerCertificate=no;'
    r'Connection Timeout=30;'
)

cursor = conn.cursor()
cursor.execute("SELECT SYSTEM_USER")
row = cursor.fetchone()
print("Connected as:", row[0])
conn.close()
```

---

# 🗄️ PostgreSQL (Using `psycopg2`)

## 1️⃣ Local PostgreSQL Connection

### 🔹 Case 1: Default Localhost Setup

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="YourDatabaseName",
    user="your_username",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
row = cursor.fetchone()
print("Connected to:", row[0])
conn.close()
```

---

### 🔹 Case 2: Using Unix Domain Socket (Linux/macOS only)

```python
import psycopg2

conn = psycopg2.connect(
    dbname="YourDatabaseName",
    user="your_username",
    password="your_password",
    host="/var/run/postgresql"
)

cursor = conn.cursor()
cursor.execute("SELECT current_database();")
row = cursor.fetchone()
print("Connected to DB:", row[0])
conn.close()
```

---

## 2️⃣ Cloud PostgreSQL (e.g., Azure or AWS RDS)

### 🔹 Case 1: Standard SSL Connection (AWS RDS / Azure DB for PostgreSQL)

```python
import psycopg2

conn = psycopg2.connect(
    host="your-cloud-host.postgres.database.azure.com",
    port=5432,
    dbname="YourDatabaseName",
    user="your_username@your-cloud-host",
    password="your_password",
    sslmode="require"
)

cursor = conn.cursor()
cursor.execute("SELECT current_user;")
row = cursor.fetchone()
print("Connected as:", row[0])
conn.close()
```

---

### 🔹 Case 2: IAM/Azure AD Auth (Advanced)

> ⚠️ This requires token-based authentication and IAM/AAD setup. Not included here due to complexity.

---

## ✅ Connection Test Template (Generic)

Use this to test your DB connection:

```python
try:
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Connection successful. Server time:", result[0])
except Exception as e:
    print("Connection failed:", e)
finally:
    conn.close()
```

---

## 🔐 Security Tips

- ❌ **Never hardcode passwords in your scripts.**
- ✅ Use environment variables or secret managers (`.env`, AWS Secrets Manager, Azure Key Vault).
- ✅ Always add `.env` to `.gitignore`.

---

## 📎 Useful Links

- [pyodbc Docs](https://learn.microsoft.com/sql/connect/python/python-sql-driver-pyodbc)
- [psycopg2 Docs](https://www.psycopg.org/docs/)
- [ODBC Drivers for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [Azure PostgreSQL](https://learn.microsoft.com/azure/postgresql/)
- [AWS RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)

---
