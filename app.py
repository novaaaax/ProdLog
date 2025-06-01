from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import threading
import schedule
import time
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yagmail

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load DB credentials from environment variables
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': 'localhost',
    'database': 'work_logs'
}

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')

def initialize_database():
    try:
        base_config = db_config.copy()
        base_config.pop('database')
        connection = mysql.connector.connect(**base_config)
        cursor = connection.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS work_logs")
        connection.database = 'work_logs'

        # Create term_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS term_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                line VARCHAR(10),
                job_number VARCHAR(50),
                qty INT,
                timestamp DATETIME
            )
        """)

        # Create tables for other work areas
        areas = ['cutting', 'prep','term', 'polish', 'scope', 'test', 'pack']
        for area in areas:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {area}_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    line VARCHAR(10),
                    job_number VARCHAR(50),
                    qty INT,
                    timestamp DATETIME
                )
            """)

        # Create order_tracker table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_tracker (
                job_number VARCHAR(50) PRIMARY KEY,
                my_date DATE,
                num_lines INT
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Initialization Error: {e}")

# Initialize DB at startup
initialize_database()

# ----------- ROUTES -----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select-line', methods=['POST'])
def select_line():
    area = request.form['area']
    return render_template('details.html', area=area)

@app.route('/submit', methods=['POST'])
def submit_data():
    area = request.form['area']
    line = request.form['line']
    job_number = request.form['job_number']
    qty = int(request.form['qty'])

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if job number exists
        cursor.execute("SELECT COUNT(*) FROM order_tracker WHERE job_number = %s", (job_number,))
        exists = cursor.fetchone()[0]
        if not exists:
            flash("This Job Number does not exist")
            return redirect(url_for('index'))

        table = f"{area}_logs"
        query = f"INSERT INTO {table} (line, job_number, qty, timestamp) VALUES (%s, %s, %s, %s)"
        data = (line, job_number, qty, datetime.now())
        cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        return f"Database Error: {e}"

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT line, SUM(qty) 
            FROM term_logs 
            GROUP BY line
        """)
        results = cursor.fetchall()
        lines = [r[0] for r in results]
        values = [r[1] for r in results]

        # Generate chart
        plt.figure(figsize=(6, 4))
        plt.bar(lines, values, color='teal')
        plt.title("Terminations by Line")
        plt.ylabel("Quantity")
        plt.savefig('static/term_chart.png')
        plt.close()

        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        return f"Dashboard Error: {e}"

    return render_template('dashboard.html')

@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        job_number = request.form['job_number']
        my_date = request.form['my_date']
        num_lines = request.form['num_lines']

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                " INSERT INTO order_tracker (job_number, my_date, num_lines) VALUES (%s, %s, %s)", 
                           (job_number, my_date, num_lines))
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            flash(f"Database Error: {e}")
            return redirect(url_for('add_job'))

        return redirect(url_for('order_tracker'))

    return render_template('add_job.html')

@app.route('/order-tracker')
def order_tracker():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM order_tracker")
        jobs = cursor.fetchall()

        data = {}
        for job in jobs:
            job_number = job[0]
            data[job_number] = {'my_date': job[1], 'num_lines': job[2]}
            for area in ['cutting', 'prep', 'term', 'polish', 'scope', 'test', 'pack']:
                cursor.execute(f"SELECT SUM(qty) FROM {area}_logs WHERE job_number = %s", (job_number,))
                total = cursor.fetchone()[0] or 0
                data[job_number][area] = total

        cursor.close()
        connection.close()
        print("Jobs fetched from order_tracker:", jobs)

        return render_template('order_tracker.html', data=data)

    except mysql.connector.Error as e:
        return f"Order Tracker Error: {e}"

# ----------- TIMED TASKS -----------

def reset_term_chart():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM term_logs")
        connection.commit()
        cursor.close()
        connection.close()
        print("Term logs reset.")
    except mysql.connector.Error as e:
        print(f"Error resetting term logs: {e}")

def save_term_chart():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT line, SUM(qty)
            FROM term_logs
            GROUP BY line
        """)
        results = cursor.fetchall()
        lines = [r[0] for r in results]
        values = [r[1] for r in results]

        plt.figure(figsize=(6, 4))
        plt.bar(lines, values, color='teal')
        plt.title("Terminations by Line")
        plt.ylabel("Quantity")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        chart_file = f'static/term_chart_{timestamp}.png'
        plt.savefig(chart_file)
        plt.close()

        cursor.close()
        connection.close()
        print("Term chart saved.")
        return chart_file
    except mysql.connector.Error as e:
        print(f"Error saving term chart: {e}")
        return None

def backup_and_email():
    try:
        dump_filename = 'backup.sql'
        cmd = ["/opt/homebrew/opt/mysql-client/bin/mysqldump", "-u", 
               db_config['user'], 
               f"-p{db_config['password']}", 
               db_config['database']]
        with open(dump_filename, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)

        message = MIMEMultipart()
        message['From'] =  EMAIL_USER
        message['To'] = EMAIL_TO
        message['Subject'] = 'Daily MySQL Schema and Term Chart'
        message.attach(MIMEText('Attached are the daily MySQL Schema and chart.'))

        with open(dump_filename, 'rb') as dump_file:
            dump_attachment = MIMEApplication(dump_file.read(), subtype="sql")
            dump_attachment.add_header('Conetent-Disposition', 'attachment', filename='backup.sql')
            message.attach(dump_attachment)

        with open('static/term_chart_{timestamp}.png', 'rb') as chart_file:
            chart_attachment = MIMEApplication(chart_file.read(), subtype="png")
            chart_attachment.add_header('Content-Disposition', 'attachment', filename='term.png')
            message.attach(chart_attachment)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(message)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error in backup_and_email function: {e}")

def run_scheduler():
    schedule.every().day.at("06:30").do(reset_term_chart)
    # change time to 16:00 for launch
    schedule.every().day.at("14:35").do(save_term_chart)
    #change time to 16:30 for launch
    schedule.every().day.at("14:35").do(backup_and_email)
    while True:
        schedule.run_pending()
        time.sleep(60)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# ----------- MAIN ENTRY -----------

if __name__ == '__main__':
    app.run(debug=True)


