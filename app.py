from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, traceback

app = Flask(__name__)
CORS(app)

scaler = joblib.load('scaler_clientes.pkl')
kmeans = joblib.load('kmeans_clientes.pkl')
etiquetas = {
    0: "Cliente frecuente",
    1: "Cliente regular",
    2: "Cliente ocasional",
    3: "Cliente esporádico"
}

@app.route('/clasificar-lote', methods=['POST'])
def clasificar_lote():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        if not isinstance(data, list):
            raise ValueError(f"Se esperaba una LISTA, llegó: {type(data)}")

        X = []
        for idx, cliente in enumerate(data):
            print(f"Procesando elemento {idx}:", cliente)
            # Aquí cliente es dict, accedemos bien:
            X.append([
                cliente['total_citas'],
                cliente['total_servicios'],
                cliente['gasto_total'],
                cliente['gasto_promedio']
            ])

        print("Matriz X antes de escalar:", X)
        X_scaled = scaler.transform(X)
        preds = kmeans.predict(X_scaled)

        # Assemblar respuesta con perfil
        for i, cliente in enumerate(data):
            cliente['perfil'] = etiquetas[preds[i]]

        print("Respuesta final:", data)
        return jsonify(data)

    except Exception as e:
        traceback.print_exc()
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
