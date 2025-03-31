
import requests
from bs4 import BeautifulSoup
import os
import zipfile

def baixar_anexos():
    try:
        print("Iniciando scraping do site da ANS para baixar os Anexos...")
        
        
        url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

        print("Acessando o site...")
        response = requests.get(url, timeout=10)
        
        print(f"Status do site: {response.status_code}")  
        if response.status_code == 200:
            print("Site acessado com sucesso!")
        else:
            print("Erro ao acessar o site.")
            
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        links_pdf = []
        for link in soup.find_all('a'):
            if ('Anexo I' in link.text or 'Anexo II' in link.text) and '.pdf' in link['href'].lower():
                links_pdf.append(link['href'])
                print(f"Link encontrado: {link.text}")
        
        print("Links que serão baixados:")
        for link in links_pdf:
            print(f"- {link}")
        
        
        os.makedirs('anexos', exist_ok=True)
        
        
        print("\nProcurando links dos Anexos...")
        for link in links_pdf:
            nome_arquivo = os.path.join('anexos', link.split('/')[-1])
            print(f"Baixando: {nome_arquivo}...")
            
            
            with open(nome_arquivo, 'wb') as f:
                f.write(requests.get(link).content)
        
        
        print("Compactando arquivos...")
        with zipfile.ZipFile('anexos.zip', 'w') as zipf:
            for arquivo in os.listdir('anexos'):
                zipf.write(os.path.join('anexos', arquivo))
        
        print("Finalizado! Verifique a pasta 'anexos' e o arquivo 'anexos.zip'")
    
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    baixar_anexos()