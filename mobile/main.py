from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import json
from kivy.network.urlrequest import UrlRequest
import webbrowser #para usar otras apps del celu (app telefono)

Builder.load_file('ZonaRoja.kv')

URL = 'https://zonarojaapi.pythonanywhere.com/api/v1/'

class PantallaBienvenida(Screen):
    def call_phone(self):
        number = "+54 9 11 5146-7001"
        webbrowser.open(f"tel:{number}")

class PantallaRespuesta(Screen):
    pass

class PantallaReporte(Screen):
    def enviar_reporte(self):
        try:
            tipo_incidencia = self.ids.input_tipoincididencia.text
            direccion = self.ids.direccion_reporte.text
            descripcion = self.ids.descripcion_reporte.text
            if tipo_incidencia == '' or direccion == '' or descripcion == '':
                mensaje_error = "Faltan datos. Completar todos los campos"
                self.ids.label_errores.text = mensaje_error
                return
            data_incidente = {
                    "tipo_reporte": tipo_incidencia,
                    "direccion_reporte": direccion,
                    "descripcion": descripcion
                    }
            json_incidente = json.dumps(data_incidente)
            url = URL + 'incidentes'
            headers = {'Content-Type': 'application/json'}
            req = UrlRequest(url, req_body=json_incidente, req_headers=headers, method='POST', on_success=self.on_post_success)
            print (json_incidente)
        except Exception as e:
            print(f"Error al intentar enviar reporte: {e}")

    def on_post_success(self, req, result):    
        try:
            id_incidencia = result
            print(f"Incidencia creada con ID: {id_incidencia}")
            provincia = self.ids.input_provincias.text
            municipio = self.ids.input_municipio.text
            localidad = self.ids.input_localidad.text
            if provincia == '' or municipio == '' or localidad == '':
                mensaje_error = "Faltan datos. Completar todos los campos"
                self.ids.label_errores.text = mensaje_error
                return   
            data_reporte = {
                    "provincia": provincia,
                    "departamento": municipio,
                    "localidad": localidad,
                    "fecha_reporte" : "2024-04-12",
                    "horario_reporte" : "04:15:00",
                    "ID_incidente" : int(id_incidencia),
                    "ID_usuario" : 17
                    }
            json_data = json.dumps(data_reporte)
            url = URL + 'reportes'
            headers = {'Content-Type': 'application/json'}
            req = UrlRequest(url, req_body=json_data, req_headers=headers, method='POST')
            print (json_data)
            self.manager.current = "respuesta"
            self.ids.input_tipoincididencia.text = ""
            self.ids.direccion_reporte.text = ""
            self.ids.descripcion_reporte.text = ""
            self.ids.input_provincias.text = ""
            self.ids.input_municipio.text = ""
            self.ids.input_localidad.text = ""
        except Exception as e:
            print(f"Error al intentar enviar reporte: {e}")


class Manager(ScreenManager):
    pantalla_bienvenida = ObjectProperty(None)
    pantalla_reporte = ObjectProperty(None)

class ZonaRoja(App):
    def build(self):
        return Manager()

ZonaRoja().run()