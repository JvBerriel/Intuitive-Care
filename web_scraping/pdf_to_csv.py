import tabula
import pandas as pd
import os
import zipfile

def encontrar_pdf_anexo():
    
    if not os.path.exists("anexos"):
        raise FileNotFoundError("Pasta 'anexos' não encontrada. Execute primeiro o scraper.py")
    
   
    arquivos = os.listdir("anexos")

    
    pdfs_anexo = [arquivo for arquivo in arquivos if "Anexo_I_" in arquivo and arquivo.endswith(".pdf")]

    if not pdfs_anexo:
        raise FileNotFoundError("Nenhum arquivo correspondente a 'Anexo_I' encontrado na pasta 'anexos'.")

    return os.path.join("anexos", pdfs_anexo[0])  

def extrair_tabela():
    try:
        print("Procurando o arquivo Anexo I...")
        pdf_path = encontrar_pdf_anexo()
        print(f"Arquivo encontrado: {pdf_path}")

        print("Extraindo tabela...")
        tabela = tabula.read_pdf(pdf_path, pages='3-181', stream=False, lattice=True, multiple_tables=True, silent=True)
        print(f"Tabela extraída com sucesso. Partes encontradas: {len(tabela)}")

        if len(tabela) > 1:
            tabela_completa = pd.concat(tabela)
            print("Tabela concatenada com sucesso")
        else:
            tabela_completa = tabela[0]

        csv_path = "rol_procedimentos.csv"
        tabela_completa.to_csv(csv_path, index=False, sep=',', encoding='utf-8-sig')  # Encoding para Excel
        print(f"\nCSV salvo em: {csv_path}")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")



def transformar_dados():
    try:
        
        tabela = pd.read_csv("rol_procedimentos.csv", encoding='utf-8-sig', sep=',')

        tabela.replace({
            "OD": "Odontológico",
            "AMB": "Ambulatorial"
        }, inplace=True)

        tabela.columns.values[3] = 'Odontológico'
        tabela.columns.values[4] = 'Ambulatorial'
        
        
        
        tabela.to_csv("rol_procedimentos_atualizado.csv", index=False, encoding='utf-8-sig', sep=',')
        
    except Exception as e:
        print(f"Erro: {e}")


def zip():
    try:
        
        
        nome_zip = f"Teste_Joao_Vitor_Costa_Berriel_Braga.zip"  
        with zipfile.ZipFile(nome_zip, 'w') as zipf:
            zipf.write("rol_procedimentos.csv")
            zipf.write("rol_procedimentos_atualizado.csv")

        
        print(f"Arquivo compactado criado: {nome_zip}")

    except Exception as e:
        print(f"Erro ao compactar o arquivo: {e}")


if __name__ == "__main__":
    extrair_tabela()
    transformar_dados()
    zip()
