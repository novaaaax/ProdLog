from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

        # Validate job_number and qty
        if not job_number.replace('-', '').isdigit() or not qty.isdigit():
            error = "Invalid input. Please enter a valid Job Number and numeric Qty."
            return render_template("details.html", area=area, error=error)

        # If valid, display confirmation (could redirect elsewhere)
        return f"Area: {area}<br>Line: {line}<br>Job Number: {job_number}<br>Qty: {qty}"

    return render_template("details.html", area=area)

if __name__ == "__main__":
    app.run(debug=True)

