from selenium import webdriver

def criar_navegador() -> webdriver.Chrome:
    """
Realiza a criação do navegador
    """

    from webdriver_manager.chrome import ChromeDriverManager 
    from selenium.webdriver.chrome.service import Service 

    try:
        servico = Service(ChromeDriverManager().install()) 
        opcoes = webdriver.ChromeOptions() 
        # opcoes.add_argument("--headless=new") 
        opcoes.add_argument('--disable-gpu')
        opcoes.add_argument('--no-sandbox')
        navegador = webdriver.Chrome(service=servico, options=opcoes) 
        return navegador
    except Exception as e:
        raise Exception(f"Impossivel criar o navegador, detalhes: {str(e)}")

def realizar_login(navegador: webdriver.Chrome, ambiente) -> webdriver.Chrome:
    """
Realiza o login no Oi360

Entrada:
    navegador(webdriver.Chrome): recebe um navegador ativo que seja comandado pelo memso.

Saída:
    O navegador com instância ativa do Oi360
    """

    from selenium.webdriver.common.by import By 

    try:
        navegador.get(ambiente)
        str(input("Pressione enter após o login ..."))
        return navegador
    except Exception as e:
        raise Exception(f"Impossivel logar no Oi360, detalhes: {str(e)}")

def escolher_tipo_cliente(navegador: webdriver.Chrome) -> webdriver.Chrome:
    """
Responde o primeiro formulário (se é varejo ou empresarial)

Entrada:
    navegador(webdriver.Chrome): recebe um navegador ativo que seja comandado pelo memso.

Saída:
    O navegador com instância ativa do Oi360 e primeiro formulário respondido
    """

    try:
        return navegador
    except Exception as e:
        raise Exception(f"Impossivel responder primeiro formulário, detalhes: {str(e)}")
