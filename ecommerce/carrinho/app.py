from flask import Flask, request, jsonify
from flask_cors import CORS
from abc import ABC, abstractmethod

app = Flask(__name__)
CORS(app)

# Interface
class CarrinhoInterface(ABC):
    @abstractmethod
    def adicionar_item(self, item): pass

    @abstractmethod
    def listar_itens(self): pass

    @abstractmethod
    def remover_item(self, item_id): pass


# Implementação concreta
class Carrinho(CarrinhoInterface):
    def __init__(self):
        self._itens = []

    def adicionar_item(self, item):
        self._itens.append(item)

    def listar_itens(self):
        return self._itens

    def remover_item(self, item_id):
        self._itens = [i for i in self._itens if i.get("id") != item_id]


# Instância global do carrinho
carrinho = Carrinho()


@app.route("/carrinho", methods=["GET"])
def listar_itens():
    return jsonify(carrinho.listar_itens())


@app.route("/carrinho", methods=["POST"])
def adicionar_item():
    item = request.json
    carrinho.adicionar_item(item)
    return jsonify({"mensagem": "Item adicionado!"})


@app.route("/carrinho/<int:item_id>", methods=["DELETE"])
def remover_item(item_id):
    carrinho.remover_item(item_id)
    return jsonify({
        "mensagem": "Item removido!",
        "restante": carrinho.listar_itens()
    })


if __name__ == "__main__":
    app.run(port=5002, debug=True)
