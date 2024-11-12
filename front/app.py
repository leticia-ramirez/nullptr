from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/reporte")
def reporte():
    return render_template("reporte.html")

@app.route("/misreportes")
def mreporte():
    return render_template("MisReportes.html")

@app.route("/app")
def descarga():
    return render_template("/descarga.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)