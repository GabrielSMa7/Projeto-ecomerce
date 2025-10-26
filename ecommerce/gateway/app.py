from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URLs dos microserviços
CATALOGO_URL = "http://localhost:5001/produtos"
CARRINHO_URL = "http://localhost:5002/carrinho"
PAGAMENTO_URL = "http://localhost:5003/pagamento"
RECOMENDACAO_URL = "http://localhost:5004"

@app.route("/")
def index():
    produtos = requests.get(CATALOGO_URL).json()
    carrinho = requests.get(CARRINHO_URL).json()
    total = sum(item["preco"] for item in carrinho)
    recs = requests.get(f"{RECOMENDACAO_URL}/recomendacoes").json()
    rec_ids = [r["product_id"] for r in recs]
    
    produtos_ordenados = sorted(
        produtos,
        key=lambda p: rec_ids.index(p["id"]) if p["id"] in rec_ids else 999
    )
    
    return render_template(
        "index.html",
        produtos=produtos_ordenados,
        carrinho=carrinho,
        total=total
    )

@app.route("/adicionar/<int:produto_id>")
def adicionar(produto_id):
    produto = next(p for p in requests.get(CATALOGO_URL).json() if p["id"] == produto_id)
    requests.post(CARRINHO_URL, json=produto)
    requests.post(f"{RECOMENDACAO_URL}/events", json={"event": "cart_add", "product_id": produto_id})
    return redirect(url_for("index"))


@app.route("/pagar")
def finalizar():
    carrinho = requests.get(CARRINHO_URL).json()
    total = sum(item["preco"] for item in carrinho)
    resposta = requests.post(PAGAMENTO_URL, json={"total": total}).json()
    return f"<h2>{resposta['mensagem']}</h2><a href='/'>Voltar</a>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)