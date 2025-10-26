from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter

app = Flask(__name__)
CORS(app)

# Pesos por tipo de evento
PESOS = {
    "cart_add": 1,
    "purchase": 2
}

produto_scores = Counter()

@app.route("/events", methods=["POST"])
def receber_evento():

    data = request.json or {}
    
    event = data.get("event")
    product_id = data.get("product_id")
    peso = PESOS[event]
    produto_scores[product_id] += peso

@app.route("/recomendacoes")
def recomendar():
    k = request.args.get("k", type=int)
    
    # Ordena por peso (maior primeiro)
    produtos_ordenados = produto_scores.most_common(k)
    
    # Formata resposta
    resultado = [
        {
            "product_id": product_id,
            "score": score
        }
        for product_id, score in produtos_ordenados
    ]
    
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(port=5004, debug=True)