from flask import Flask, jsonify
from flask_cors import CORS
from abc import ABC, abstractmethod

app = Flask(__name__)
CORS(app)

# Interface do catálogo de produtos
class ProdutoCatalogoInterface(ABC):
    @abstractmethod
    def listar_produtos(self):
        pass

    @abstractmethod
    def adicionar_produto(self, produto):
        pass

# Implementação concreta do catálogo
class ProdutoCatalogo(ProdutoCatalogoInterface):
    def __init__(self):
        self._produtos = [
            {"id": 1, "nome": "Notebook", "preco": 3500},
            {"id": 2, "nome": "Smartphone", "preco": 1800},
            {"id": 3, "nome": "Fone de ouvido", "preco": 250}
        ]

    def listar_produtos(self):
        return self._produtos

    def adicionar_produto(self, produto):
        self._produtos.append(produto)

# Instância do catálogo
catalogo = ProdutoCatalogo()

@app.route("/produtos")
def listar_produtos():
    return jsonify(catalogo.listar_produtos())

if __name__ == "__main__":
    app.run(port=5001)
