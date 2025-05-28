from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os


db_password = os.environ.get("passowrd")
# Use db_password in your SQL connection


app = Flask(__name__)

# MySQL connection config (no database yet)
db_config_base = {
    'host': 'localhost',
    'user': 'root',               
    'password': 'your_password',  
}

db_name = 'work_logs'

# Schema for each table
table_schema = """
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line VARCHAR(10),
    job_number VARCHAR(50),
    qty INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

def init_db():
    # Connect without specifying database
    connection = mysql.connector.connect(**db_config_base)
    cursor = connection.cursor()

    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    connection.commit()

    # Select the database
    cursor.execute(f"USE {db_name}")

    # List of tables (work areas)
    tables = ['cutting_prep', 'term', 'polish', 'scope', 'test', 'pack']

    # Create tables if not exist
    for table in tables:
        cursor.execute(table_schema.format(table_name=table))
    connection.commit()

    cursor.close()
    connection.close()

# Call the function on app start
init_db()

# Now full db config with database name
db_config = {
    **db_config_base,
    'database': db_name
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_area = request.form.get("workArea")
        if selected_area:
            return redirect(url_for('details', area=selected_area))
    return render_template("index.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    area = request.args.get("area", None)
    if not area:
        return redirect(url_for('index'))

    if request.method == "POST":
        line = request.form.get("line")
        job_number = request.form.get("job_number")
        qty = request.form.get("qty")

        if not job_number.replace('-', '').isdigit() or not qty.isdigit():
            error = "Invalid input. Please enter a valid Job Number and numeric Qty."
            return render_template("details.html", area=area, error=error)

        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            table_name = area.replace(" ", "_").lower()

            insert_query = f"""
                INSERT INTO {table_name} (line, job_number, qty)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (line, job_number, int(qty)))
            connection.commit()

        except mysql.connector.Error as err:
            return f"❌ Database Error: {err}"
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

        return f"✅ Saved to <strong>{table_name}</strong>: Line {line}, Job #{job_number}, Qty {qty}"

    return render_template("details.html", area=area)

if __name__ == "__main__":
    app.run(debug=True)
