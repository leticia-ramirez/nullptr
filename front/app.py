from flask import Flask, render_template, request, redirect, jsonify, url_for
import requests
import pprint
app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/api/v1/"

@app.route("/", methods=["GET", "POST"]) #endpoint reporte
def home():
    try:
        response = requests.get(API_URL+'reportesNovedades')
        response.raise_for_status()
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error traer data: {e}")
        reportes = []

    return render_template("home.html", reportes = reportes)

@app.route("/buscarzona", methods=["GET", "POST"])
def buscar():
    # response = f"{API_URL}reportes/localidad"
    # busqueda=request.args.get('busqueda')
    # if busqueda:
    #     url = f"{response}/{busqueda}"
    #     response = requests.get(url)

    # if response.status_code != 200:
    #     return 400
    
    # if request.method =="GET":
    #     data = {
    #         "tipo_reporte" : request.form.get("incidencia"),
    #     }
    #     try:
    #         response = requests.get(API_URL+'reportes/tipo/' + data["tipo_reporte"])
    #         response.raise_for_status()
          
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error pushing data: {e}")

    #         return render_template("buscar_zona.html")

    return render_template("buscar_zona.html")


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
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        reportes = []
    return render_template("MisReportes.html", reportes = reportes)

@app.route('/modificar/<int:id>', methods=['GET','POST', 'PUT'])#endpoint modificar reporte (aun no funciona)
def modificar(id):
    datos=requests.get(API_URL+'reportes/id/'+str(id)).json()

    if request.method=='POST':
        ID = request.form['id_reporte']
        ID_usuario= request.form['ID_usuario']
        localidad= request.form['localidad']
        direccion_reporte= request.form['direccion_reporte']
        descripcion = request.form['descripcion']
        tipo_reporte = request.form['tipo_reporte']
        fecha_reporte = request.form['fecha_reporte']
    
        response = f"{API_URL}reportes/id/{id}"
        params = None

        if localidad is not None:
            params = { 
                'ID_reporte' :ID,
                'ID_usuario':ID_usuario,
                'localidad': localidad,
                'direccion_reporte': direccion_reporte,
                'descripcion' : descripcion,
                'tipo_reporte' : tipo_reporte,
                'fecha_reporte' : fecha_reporte
            }
            try:
                response = requests.put(response, data=params) #url?name:character_name la funcion agrega el ?
                response.raise_for_status()
                if response:
                    return redirect(url_for('mreporte'))
                    
            except requests.exceptions.RequestException as e:
                print(f"Error pushing data: {e}")
                
    return render_template('modificar.html', datos=datos[0], id=id)

@app.route("/elimacion/<int:id>") #endpoint eliminar reportes de mreporte
def eliminar_reporte(id):
    try:
        response = requests.delete(API_URL+'reportes/'+str(id))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return redirect(url_for("mreporte"))

@app.route("/misreportes/<id>")
def mreporte_id(id): #endpoint para mostrar todos los reportes
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

@app.route("/contacto", methods=['POST','GET'])
def contacto():
    return render_template("contacto.html")

@app.errorhandler(404)
def error(e):
    return render_template('error.html')

@app.errorhandler(400)
def error(e):
    return render_template('error400.html')

@app.errorhandler(500)
def error(e):
    return render_template('error500.html')

if __name__ == "__main__":
    app.run(debug=True, port="5001")