from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import webbrowser

app = Flask(__name__)
CORS(app)  


try:
    df_operadoras = pd.read_csv('database/Relatorio_cadop.csv', encoding='utf-8', sep=';')
    df_operadoras.columns = df_operadoras.columns.str.strip().str.lower()
    print("✅ Dataset carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar dataset: {str(e)}")
    df_operadoras = pd.DataFrame()  

@app.route('/')
def home():
    
    return """
    <h1>API de Operadoras de Saúde</h1>
    <p>Endpoints disponíveis:</p>
    <ul>
        <li><a href="/buscar-operadoras">/buscar-operadoras</a> - Lista todas as operadoras</li>
        <li><a href="/buscar-operadoras?query=saude">/buscar-operadoras?query=saude</a> - Exemplo de busca</li>
    </ul>
    """

@app.route('/buscar-operadoras', methods=['GET'])
def buscar_operadoras():
    try:
        query = request.args.get('query', '').strip().lower()
        
        # Validações
        if len(query) > 100:
            return jsonify({
                "error": "Query muito longa",
                "message": "O termo de busca deve ter no máximo 100 caracteres"
            }), 400
            
        if df_operadoras.empty:
            return jsonify({
                "error": "Dados indisponíveis",
                "message": "O dataset de operadoras não pôde ser carregado"
            }), 503
            
        # Lógica de busca
        if not query:
            resultados = df_operadoras.head(100)  # Limita resultados sem query
        else:
            resultados = df_operadoras[
                df_operadoras['nome_fantasia'].astype(str).str.lower().str.contains(query, na=False) |
                df_operadoras['razao_social'].astype(str).str.lower().str.contains(query, na=False) |
                df_operadoras['registro_ans'].astype(str).str.contains(query, na=False) |
                df_operadoras['cnpj'].astype(str).str.contains(query, na=False)
            ]
        
        # Formata resposta
        return jsonify({
            "success": True,
            "count": len(resultados),
            "data": resultados.fillna('').to_dict(orient='records')
        })
        
    except Exception as e:
        return jsonify({
            "error": "Erro interno",
            "message": str(e)
        }), 500

def abrir_navegador():
    
    webbrowser.open_new('http://localhost:5000/buscar-operadoras')

if __name__ == '__main__':
    
    abrir_navegador()
    
    
    print("\n🌐 API Flask rodando em:")
    print("   - Local: http://localhost:5000")
    print("   - Busca: http://localhost:5000/buscar-operadoras?query=termo")
    print("\n🔌 Pressione CTRL+C para encerrar")
    
    
    app.run(host='127.0.0.1', port=5000, debug=True)