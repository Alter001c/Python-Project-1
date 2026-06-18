from flask import Flask, request, jsonify
from flask_cors import CORS
from Producto import Producto
from Inventario import Inventario
from Carrito import Carrito
from Factura import Factura
from GestorFacturas import GestorFacturas
import json
import os

app = Flask(__name__)
CORS(app)

# Inicializar datos
inventario = Inventario()
gestor_facturas = GestorFacturas()
next_invoice_number = 1

def cargar_datos():
    global next_invoice_number
    # Cargar inventario
    try:
        with open("inventario.json", "r") as f:
            data = json.load(f)
            for p in data:
                inventario.addProducto(Producto(**p))
    except FileNotFoundError:
        # Datos de ejemplo
        inventario.addProducto(Producto("Collar de perlas", 10.0, "unidad"))
        inventario.addProducto(Producto("Hilo de nylon", 2.0, "metro"))
        inventario.addProducto(Producto("Cuentas de cristal", 5.0, "unidad"))
        inventario.addProducto(Producto("Alambre de plata", 3.5, "metro"))
        guardar_inventario()

    # Cargar facturas
    try:
        with open("facturas.json", "r") as f:
            data = json.load(f)
            for fd in data:
                items = [(Producto(**p), c) for p, c in fd["items"]]
                carrito_temp = type("CarritoTemp", (), {"items": items})()
                factura = Factura(fd["numero"], carrito_temp)
                factura.fecha = fd["fecha"]
                factura.total = fd["total"]
                gestor_facturas.facturas.append(factura)
                
                if gestor_facturas.facturas:
                    max_num = max(f.numero for f in gestor_facturas.facturas)
                    next_invoice_number = max_num + 1
    except FileNotFoundError:
        pass

def guardar_inventario():
    with open("inventario.json", "w") as f:
        json.dump([p.__dict__ for p in inventario.productos], f, default=str)

def guardar_facturas():
    data = []
    for f in gestor_facturas.facturas:
        data.append({
            "numero": f.numero,
            "fecha": str(f.fecha),
            "items": [(p.__dict__, c) for p, c in f.items],
            "total": f.total
        })
    with open("facturas.json", "w") as f:
        json.dump(data, f, default=str)

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify([p.__dict__ for p in inventario.productos])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    producto = Producto(
        nombre=data['nombre'],
        precio=float(data['precio']),
        unidad_medida=data.get('unidad_medida', 'unidad'),
        descripcion=data.get('descripcion', ''),
        foto=data.get('foto')
    )
    inventario.addProducto(producto)
    guardar_inventario()
    return jsonify(producto.__dict__)

@app.route('/api/products/<nombre>', methods=['DELETE'])
def delete_product(nombre):
    producto = inventario.searchProducto(nombre)
    if producto:
        inventario.removeProducto(producto)
        guardar_inventario()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Product not found'}), 404

@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    data = []
    for f in gestor_facturas.facturas:
        data.append({
            'numero': f.numero,
            'fecha': str(f.fecha),
            'items': [{'producto': p.__dict__, 'cantidad': c} for p, c in f.items],
            'total': f.total
        })
    return jsonify(data)

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    global next_invoice_number
    data = request.json
    
    # Crear carrito temporal
    carrito_temp = Carrito()
    for item in data['items']:
        p = Producto(**item['producto'])
        carrito_temp.addChart(p, item['cantidad'])
    
    factura = Factura(next_invoice_number, carrito_temp)
    gestor_facturas.facturas.append(factura)
    next_invoice_number += 1
    guardar_facturas()
    
    return jsonify({
        'numero': factura.numero,
        'fecha': str(factura.fecha),
        'items': [{'producto': p.__dict__, 'cantidad': c} for p, c in factura.items],
        'total': factura.total
    })

if __name__ == '__main__':
    cargar_datos()
    app.run(debug=True, port=5000)