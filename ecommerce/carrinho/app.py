from flask import Flask, request, jsonify
from flask_cors import CORS
from abc import ABC, abstractmethod

app = Flask(__name__)
CORS(app)

# Interface do carrinho
class CarrinhoInterface(ABC):
    @abstractmethod
    def adicionar_item(self, item):
        pass

    @abstractmethod
    def listar_itens(self):
        pass

# Implementação concreta do carrinho
class Carrinho(CarrinhoInterface):
    def __init__(self):
        self._itens = []

    def adicionar_item(self, item):
        self._itens.append(item)

    def listar_itens(self):
        return self._itens

# Instância do carrinho
carrinho = Carrinho()

@app.route("/carrinho", methods=["GET"])
def ver_carrinho():
    return jsonify(carrinho.listar_itens())

@app.route("/carrinho", methods=["POST"])
def adicionar_ao_carrinho():
    item = request.json
    carrinho.adicionar_item(item)
    return jsonify({"mensagem": "Item adicionado ao carrinho!"})

if __name__ == "__main__":
    app.run(port=5002)
