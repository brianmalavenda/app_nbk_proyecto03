import sqlite3
import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sanmartin_proyects.db')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Asegurar que Flask use el directorio correcto
app.template_folder = TEMPLATE_DIR

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabla de personas
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT,
                 apellido TEXT,
                 direccion TEXT,
                 utm_x REAL,
                 utm_y REAL)''')
    
    # Tabla de barrios
    c.execute('''CREATE TABLE IF NOT EXISTS barrios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT,
                 coordenadas TEXT)''')
    
    # Insertar datos de prueba solo si no existen
    c.execute("SELECT COUNT(*) FROM personas")
    if c.fetchone()[0] == 0:
        personas = [
            ('Yolanda', 'Nieves', 'Calle Primavera 123', 445000, 4455000),
            ('Carlos', 'Gomez', 'Avenida Central 456', 446000, 4456000),
            ('Maria', 'Lopez', 'Calle Roble 789', 447000, 4457000)
        ]
        c.executemany('INSERT INTO personas (nombre, apellido, direccion, utm_x, utm_y) VALUES (?,?,?,?,?)', personas)
    
    c.execute("SELECT COUNT(*) FROM barrios")
    if c.fetchone()[0] == 0:
        barrios = [
            ('Centro', '[[445500, 4455500], [446500, 4455500], [446500, 4456500], [445500, 4456500]]'),
            ('Norte', '[[446500, 4455500], [447500, 4455500], [447500, 4456500], [446500, 4456500]]'),
            ('Sur', '[[444500, 4454500], [445500, 4454500], [445500, 4455500], [444500, 4455500]]')
        ]
        c.executemany('INSERT INTO barrios (nombre, coordenadas) VALUES (?,?)', barrios)
    
    conn.commit()
    conn.close()

init_db()

def punto_en_poligono(x, y, poligono):
    n = len(poligono)
    dentro = False
    p1x, p1y = poligono[0]
    for i in range(1, n + 1):
        p2x, p2y = poligono[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        dentro = not dentro
        p1x, p1y = p2x, p2y
    return dentro

def obtener_barrio_por_utm(x, y):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, nombre, coordenadas FROM barrios')
    barrios = c.fetchall()
    
    for barrio in barrios:
        id_barrio, nombre, coords_str = barrio
        try:
            poligono = json.loads(coords_str)
            if punto_en_poligono(x, y, poligono):
                return nombre
        except json.JSONDecodeError:
            continue
    
    return "Barrio no encontrado"

@app.route('/')
def index():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, nombre, apellido FROM personas')
        personas = c.fetchall()
        conn.close()
        return render_template('index.html', personas=personas)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/obtener_barrio/<int:persona_id>')
def obtener_barrio(persona_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT utm_x, utm_y FROM personas WHERE id = ?', (persona_id,))
        resultado = c.fetchone()
        conn.close()
        
        if resultado:
            utm_x, utm_y = resultado
            barrio = obtener_barrio_por_utm(utm_x, utm_y)
            return jsonify({'barrio': barrio})
        
        return jsonify({'error': 'Persona no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug')
def debug():
    return f"""
    <h1>Debug Info</h1>
    <p>Directorio base: {BASE_DIR}</p>
    <p>Ruta DB: {DB_PATH}</p>
    <p>Directorio plantillas: {TEMPLATE_DIR}</p>
    <p>Archivos en directorio plantillas: {os.listdir(TEMPLATE_DIR)}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)