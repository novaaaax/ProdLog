from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    selected_area = None
    if request.method == "POST":
        selected_area = request.form.get("workArea")
    return render_template("index.html", selected_area=selected_area)

if __name__ == "__main__":
    app.run(debug=True)
