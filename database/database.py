# app.py
import sqlite3
from flask import Flask, render_template, request, jsonify

# Crear y poblar la base de datos
def init_db():
    conn = sqlite3.connect('sanmartin_proyects.db')
    c = conn.cursor()
    
    # Tabla de personas
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
                 id INTEGER PRIMARY KEY,
                 nombre TEXT,
                 apellido TEXT,
                 direccion TEXT)''')
    
    # Tabla de barrios
    c.execute('''CREATE TABLE IF NOT EXISTS barrios (
                 id INTEGER PRIMARY KEY,
                 nombre TEXT,
                 coordenadas TEXT)''')  # Almacenaremos JSON con las coordenadas
    
    # Insertar datos de prueba
    # Personas
    personas = [
        ('Yolanda', 'Nieves', 'grito de alcorta y alessandri', 'moron'),
        ('Carlos', 'Gomez', 'Avenida Central 456', 'moron'),
        ('Maria', 'Lopez', 'Calle Roble 789', 'moron')
    ]
    c.executemany('INSERT INTO personas (nombre, apellido, direccion, utm_x, utm_y) VALUES (?,?,?,?,?)', personas)
    
    # Barrios (coordenadas como lista de puntos [x,y])
    barrios = [
        ('Centro', '[[445500, 4455500], [446500, 4455500], [446500, 4456500], [445500, 4456500]]'),
        ('Norte', '[[446500, 4455500], [447500, 4455500], [447500, 4456500], [446500, 4456500]]'),
        ('Sur', '[[444500, 4454500], [445500, 4454500], [445500, 4455500], [444500, 4455500]]')
    ]
    c.executemany('INSERT INTO barrios (nombre, coordenadas) VALUES (?,?)', barrios)
    
    conn.commit()
    conn.close()