from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/api/v1/"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = {
            "tipo_reporte" : request.form.get("incidencia"),
        }
        try:
            response = requests.get(API_URL+'reportes/tipo/' + data["tipo_reporte"])
            response.raise_for_status()
            datos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
            datos = []

            return render_template("home.html", datos = datos)
    return render_template("home.html")

@app.route("/reporte", methods=['GET','POST'])
def reporte():
    if request.method == "POST":
        data = {
            "ID" : 123,
            "ubicacion": request.form.get("localidad"),
            "descripcion" : request.form.get("mensaje"),
            "tipo_reporte" : request.form.get("incidencia"),
            "fecha_reporte" : request.form.get("fecha"),
            "id_usuario" : 456
        }
        try:
            response = requests.post(API_URL+'reportes', json = data)
            response.raise_for_status()
            datos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
            datos = []

            return render_template("reporte.html", datos = datos)
    return render_template("reporte.html")

@app.route("/misreportes")
def mreporte():
    try:
        response = requests.get(API_URL+'reportes')
        response.raise_for_status()
        datos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        datos = []

        return render_template("MisReportes.html", datos = datos)

@app.route("/misreportes/<id>")
def mreporte_id(id):
    try:
        response = requests.get(API_URL+'reportes/id/'+id)
        response.raise_for_status()
        datos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        datos = []

        return render_template("MisReportes.html", datos = datos)

@app.route("/download")
def download():
    return render_template("/download.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


if __name__ == "__main__":
    app.run(debug=True, port="5001")