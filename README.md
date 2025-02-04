# MySQL Manager

A simple GUI-based MySQL database manager built with **PyQt5** and **PyMySQL**. This application allows you to connect to a MySQL database, execute SQL queries, view results in a table format, and update data directly within the table.

## Features
- **Database Connection:** Enter MySQL host, username, password, and database name to establish a connection.
- **Query Execution:** Write and execute SQL queries.
- **Result Display:** View query results in an editable table.
- **Data Update:** Modify data directly in the result table, with automatic updates to the database.
- **Logging:** Real-time logs for connection status, query execution, and data updates.

## Prerequisites
- Python 3.x
- Required Python libraries:
  - PyQt5
  - PyMySQL

## Installation
1. Clone the repository or download the script.
2. Install the required libraries:
   ```bash
   pip install PyQt5 pymysql
   ```

## Usage
1. Run the script:
   ```bash
   python mysql_manager.py
   ```
2. Fill in the database connection details:
   - **Host:** Your MySQL server host (e.g., `localhost`)
   - **User:** Your MySQL username
   - **Password:** Your MySQL password
   - **Database:** The database you want to connect to
3. Click **Connect** to establish a connection.
4. Enter an SQL query in the text box (e.g., `SELECT * FROM users;`).
5. Click **Execute** to run the query.
6. View and edit data directly in the table. Changes are automatically updated in the database.

## Example
```sql
SELECT * FROM employees;
```
You can modify any cell, and the changes will be reflected in the MySQL database automatically.

## Notes
- The first column is assumed to be the primary key for update operations.
- Only simple `SELECT` and `UPDATE` queries are supported for editing functionality.

## License
This project is open-source and available under the MIT License.

