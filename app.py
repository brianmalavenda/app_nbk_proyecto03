import json
import os
from flask import Flask, render_template, request, jsonify
from shapely.geometry import Polygon, Point
import requests

app = Flask(__name__)
# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, 'sanmartin_proyects.db')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# Asegurar que Flask use el directorio correcto
app.template_folder = TEMPLATE_DIR

class Persona(object):
    def __init__(self, id, nombre, apellido, direccion, localidad):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.localidad = localidad
        print(self)
    
    def __str__(self):
        return "Nmbre %s %s: Vive en %s, %s" % (self.nombre, self.apellido, self.direccion, self.localidad )
    
class Coordenadas(object):
    def __init__(self, latitud, longitud):
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        print(self)
    
    def __str__(self):
        return "Latitud: %s, Longitud: %s" % (self.latitud, self.longitud)

def cargar_personas():
    try:
        with open('./documents/personas.json', 'r', encoding='utf-8') as f:
            personas_data = json.load(f)
            return [Persona(**p) for p in personas_data]
    except Exception as e:
        print(f"Error cargando personas: {e}")
        return []

# Cargar barrios desde JSON
def cargar_barrios():
    try:
        with open('./documents/barrios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando barrios: {e}")
        return {}
# Cargar datos al iniciar
personas_list = cargar_personas()
barrios_list = cargar_barrios()

# Función buscar_persona corregida
def buscar_persona(persona_id):
    # Convertir a string para manejar diferentes formatos
    persona_id = str(persona_id)
    for persona in personas_list:
        if str(persona.id) == persona_id:
            print(f"✅ Persona encontrada: {persona.nombre} {persona.apellido}")
            return persona
    
    print(f"\n❌ Persona con ID '{persona_id}' no encontrada")
    return None

@app.route('/direccion/<int:persona_id>')
def buscar_direccion(direccion, localidad):
    res = requests.get("https://apis.datos.gob.ar/georef/api/direcciones",
    params={"direccion": direccion, "provincia": "06", "localidad": localidad}, timeout=5)
    jsonbody = res.json()
    if res.status_code != 200 or jsonbody['cantidad'] == 0:
        print(f"\n❌ Dirección '{direccion}, {localidad}' no encontrada")
        return None
    ubicacion = jsonbody["direcciones"][0]["ubicacion"]
    return Coordenadas(ubicacion["lat"], ubicacion["lon"])

@app.route('/')
def index():
    try:
        print("Renderizando plantilla index.html")
        # Renderizar la plantilla con los datos de las personas
        return render_template('index.html', personas=personas_list)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/obtener_barrio/<int:persona_id>')
def obtener_barrio(persona_id):
    try:
        persona = buscar_persona(persona_id)
        if not persona:
            return jsonify({"error": "Persona no encontrada"}), 404
        
        direccion = buscar_direccion(persona.direccion, persona.localidad)
        if not direccion:
            return jsonify({"error": "Dirección no encontrada"}), 404

        punto = Point(direccion.longitud, direccion.latitud)

        for barrio in barrios_list:           
            polygon = Polygon(barrio['coordinates'])
                  
            if polygon.contains(punto):
                print("✅ El punto está dentro del área.")
                # Enviar al front un json con el nombre del barrio
                # que esta esperando un "data" con el atributo "barrio"
                # .done(function(data) {
                # $('#barrio').val(data.barrio);
                return jsonify({'barrio': barrio['name']})
            else:
                print("❌ El punto NO está dentro del área.")
        return jsonify({'barrio': 'No existe'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)