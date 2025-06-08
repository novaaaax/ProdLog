from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, date
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import threading
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# will add weasprint feature later (send snapshots of tracker)
# from weasyprint import HTML
from io import BytesIO
import zipfile

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

        cursor.execute("CREATE DATABASE IF NOT EXISTS work_logs")
        connection.database = 'work_logs'

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS term_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                line VARCHAR(10),
                job_number VARCHAR(50),
                qty INT,
                timestamp DATETIME
            )
        """)

        areas = ['cutting', 'prep', 'term', 'polish', 'scope', 'test', 'pack']
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

initialize_database()

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

        cursor.execute("SELECT line, SUM(qty) FROM term_logs GROUP BY line")
        results = cursor.fetchall()
        lines = [r[0] for r in results]
        values = [r[1] for r in results]

        #trying chart with JavaScript 
        #plt.figure(figsize=(6, 4))
        #plt.bar(lines, values, color='teal')
        #plt.title("Terminations by Line")
        #plt.ylabel("Quantity")
        #plt.savefig('static/term_chart.png')
        #plt.close()

        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        return f"Dashboard Error: {e}"

    return render_template('dashboard.html', labels=lines, values=values)

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
                "INSERT INTO order_tracker (job_number, my_date, num_lines) VALUES (%s, %s, %s)",
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

        # Posting jobs to order_tracker by soonest date
        cursor.execute("SELECT * FROM order_tracker ORDER by my_date ASC")
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
        # Now passing today's date to order_tracker.html when calling function
        return render_template('order_tracker.html', data=data, today=date.today())
    except mysql.connector.Error as e:
        return f"Order Tracker Error: {e}"

def save_order_tracker_chart():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT job_number, num_lines FROM order_tracker")
        jobs = cursor.fetchall()

        job_labels = []
        area_totals = {'cutting': [], 'prep': [], 'term': [], 'polish': [], 'scope': [], 'test': [], 'pack': []}

        for job_number, _ in jobs:
            job_labels.append(job_number)
            for area in area_totals.keys():
                cursor.execute(f"SELECT SUM(qty) FROM {area}_logs WHERE job_number = %s", (job_number,))
                total = cursor.fetchone()[0] or 0
                area_totals[area].append(total)

        fig, ax = plt.subplots(figsize=(10, 6))
        bottom = [0] * len(job_labels)
        for area, values in area_totals.items():
            ax.bar(job_labels, values, bottom=bottom, label=area)
            bottom = [sum(x) for x in zip(bottom, values)]

        ax.set_title("Order Tracker - Quantity by Job")
        ax.set_ylabel("Total Quantity")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_file = f'static/order_tracker_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.png'
        plt.savefig(chart_file)
        plt.close()
        cursor.close()
        connection.close()
        return chart_file
    except Exception as e:
        print(f"Error saving Order Tracker chart: {e}")
        return None

def backup_and_email():
    try:
        chart_file_path = save_order_tracker_chart()
        if not chart_file_path or not os.path.exists(chart_file_path):
            raise FileNotFoundError("Order tracker chart file not found.")

        message = MIMEMultipart()
        message['From'] = EMAIL_USER
        message['To'] = EMAIL_TO
        message['Subject'] = 'Daily Order Tracker Chart'
        message.attach(MIMEText('Attached is the daily Order Tracker chart.'))

        with open(chart_file_path, 'rb') as img:
            img_attachment = MIMEApplication(img.read(), Name=os.path.basename(chart_file_path))
            img_attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(chart_file_path)}"'
            message.attach(img_attachment)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(message)

        print("Email sent successfully with Order Tracker chart.")
    except Exception as e:
        print(f"Error in backup_and_email function: {e}")

def run_scheduler():
    # will work on this feature later
    # schedule.every().day.at("06:30").do(lambda: print("Reset Term Chart Placeholder"))
    # Change time to 4:30 for launch
    schedule.every().day.at("17:17").do(backup_and_email)
    while True:
        schedule.run_pending()
        time.sleep(60)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
