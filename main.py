import subprocess
from pathlib import Path
import webbrowser
import time

BASE_DIR = Path(__file__).parent

def executar_comando(comando, pasta=None):
    
    try:
        subprocess.run(comando, cwd=pasta, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def limpar_tela():
    
    print("\n" * 50)  

def menu():
    while True:
        limpar_tela()
        print("\n=== MENU PRINCIPAL ===")
        print("1. Baixar anexos")
        print("2. Converter PDFs em CSV")
        print("3. Iniciar sistema completo")
        print("4. Sair")
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == "1":
            limpar_tela()
            print("=== BAIXANDO ANEXOS ===")
            if executar_comando('python web_scraping/scraper.py'):
                print("\nDownload concluído com sucesso!")
            input("\nPressione Enter para voltar ao menu...")
            
        elif opcao == "2":
            limpar_tela()
            print("=== CONVERTENDO PDFs ===")
            if executar_comando('python web_scraping/pdf_to_csv.py'):
                print("\nConversão concluída com sucesso!")
            input("\nPressione Enter para voltar ao menu...")
            
        elif opcao == "3":
            limpar_tela()
            print("=== INICIANDO SISTEMA ===")
            
             
            subprocess.Popen('python api/server.py', shell=True)
            
            
            subprocess.Popen('npm run serve', shell=True, cwd='frontend')
            
            time.sleep(2)  
            webbrowser.open('http://localhost:8080')
            print("\nServiços iniciados com sucesso!")
            print("Frontend: http://localhost:8080")
            input("\nPressione Enter para voltar ao menu...")
            
        elif opcao == "4":
            print("\nSaindo do sistema...")
            break
            
        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    menu()