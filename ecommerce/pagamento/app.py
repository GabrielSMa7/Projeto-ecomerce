
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/pagamento", methods=["POST"])
def realizar_pagamento():
    dados = request.json
    total = dados.get("total", 0)
    return jsonify({"mensagem": f"Pagamento-Atualizado de R${total:.2f} realizado com sucesso!!!"})

if __name__ == "__main__":
    app.run(port=5003)
