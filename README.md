# Database Connection Utility

This module provides utility functions to connect to databases using either **Azure SQL**, **Local SQL Server**, or **PostgreSQL**. 

It uses `pyodbc` for SQL connections and `psycopg2` for PostgreSQL connections. Azure-based connections are authenticated using `DefaultAzureCredential` from the Azure Identity SDK.

---

## 📁 File Structure

```
src/
  └── database_utilities/
        └── DatabaseConnection.py
```

---

## 📦 Prerequisites

Install the required dependencies:

```bash
pip install pyodbc psycopg2 azure-identity fastapi
```

Ensure your environment variables/configuration values are correctly set in:

- `SQL_DB_CONFIG` (for Azure/Local SQL)
- `POSTGRES_DB_CONFIG` (for PostgreSQL)

---

## ⚙️ Configuration Examples

### `SQL_DB_CONFIG` (Dictionary)
```python
SQL_DB_CONFIG = {
    'sql_driver': '{ODBC Driver 17 for SQL Server}',
    'sql_server': 'your-sql-server.database.windows.net',
    'sql_client_id': 'your-managed-identity-client-id'
}
```

### `POSTGRES_DB_CONFIG` (Dictionary)
```python
POSTGRES_DB_CONFIG = {
    'user': 'your_user',
    'password': 'your_password',
    'host': 'your_postgres_host',
    'dbname': 'your_database_name',
    'ssl_mode': 'require'
}
```

---

## 🧠 How it Works

### `DatabaseConnection` Class

This class includes:
- `get_sql_conn()`: Connects to SQL Server using either Azure token-based or local string-based authentication.
- `get_postgres_conn()`: Connects to PostgreSQL using username/password-based authentication.

---

## 🔌 SQL Server Connection

### ✅ Azure SQL Connection

Uncomment the following block in `get_sql_conn()` to connect to Azure SQL:

```python
credential = DefaultAzureCredential(managed_identity_client_id=SQL_DB_CONFIG["sql_client_id"])
token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f"<I{len(token)}s", len(token), token)

conn_string = (
    f"Driver={SQL_DB_CONFIG['sql_driver']};"
    f"Server={SQL_DB_CONFIG['sql_server']},1433;"
    f"Database=Management;"
    f"UID={SQL_DB_CONFIG['sql_client_id']};"
    f"Authentication=ActiveDirectoryMsi;"
    f"Encrypt=yes;"
)

sql_conn = pyodbc.connect(conn_string, attrs_before={sql_copt_ss_access_token: token_struct})
```

### ✅ Local SQL Server Connection

To connect to a local SQL Server using username/password:

```python
conn_string = (
    f"Driver={SQL_DB_CONFIG['sql_driver']};"
    f"Server={SQL_DB_CONFIG['sql_server']};"
    f"TrustServerCertificate=yes;"
    f"Encrypt=yes;"
)

sql_conn = pyodbc.connect(conn_string)
```

---

## 🐘 PostgreSQL Connection

PostgreSQL is connected using `psycopg2` and the connection string is formed as:

```python
db_uri = (
    f"postgresql://{POSTGRES_DB_CONFIG['user']}:{password}"
    f"@{POSTGRES_DB_CONFIG['host']}/{POSTGRES_DB_CONFIG['dbname']}"
    f"?sslmode={POSTGRES_DB_CONFIG['ssl_mode']}"
)

postgres_conn = psycopg2.connect(db_uri)
```

---

## 🚀 Usage

```python
from database_utilities.DatabaseConnection import DatabaseConnection

# Initialize
db_connection = DatabaseConnection()

# For SQL Server
sql_conn = db_connection.get_sql_conn()

# For PostgreSQL
postgres_conn = db_connection.get_postgres_conn()
```

---

## ✅ Output

Successful connection logs:
```bash
[INFO] Token obtained successfully
[INFO] Connecting to the database...
[INFO] Connection established successfully.
```

---

## 🧪 Testing

You can test by running:

```bash
python database_utilities/DatabaseConnection.py
```

Make sure `if __name__ == "__main__"` block is enabled for testing both SQL and PostgreSQL connections.

---

## 📄 License

This utility is internal to your project. Update with a license if sharing externally.

---

## ✍️ Author

Gopichand
