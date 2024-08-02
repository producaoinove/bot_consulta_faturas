from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def criar_navegador() -> webdriver.Chrome:
    """
Realiza a criação do navegador
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service 
    from selenium.webdriver.chrome.options import Options

    try:
        opcoes = Options()
        # opcoes.add_argument("--headless=new")
        opcoes.add_argument('--disable-gpu')
        opcoes.add_argument('--no-sandbox')
        browser = webdriver.Chrome(options=opcoes)
        return browser
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

    try:
        navegador.get(ambiente)        
        str(input("Pressione enter após o login ..."))
        return navegador
    except Exception as e:
        raise Exception(f"Impossivel logar no Oi360, detalhes: {str(e)}")

def escolher_tipo_cliente(navegador: webdriver.Chrome):
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

def search_doc(browser: webdriver.Chrome, documento: str, tipo: str, logging):
    status = ""
    if tipo == 'EMPRESARIAL':
        cnpj_input = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, 'AuxiliarCOD_IDENT_PESSOA'))
        )
        cnpj_input.click()
        cnpj_input.send_keys(documento)
        browser.implicitly_wait(1)
        
        cnpj_search_button = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CT"]/div/div/div/div[1]/div/div/div/div[2]/span/button'))
        )
        cnpj_search_button.click()
        browser.implicitly_wait(3)
        
        try:
            product_button = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, '//*[@id="CT"]/div/div/div'))
            )
            if product_button.is_displayed:
                product_button.click()
                browser.implicitly_wait(5)
        except:
            logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao")
        try:
            new_client_div = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Novo Cliente')]"))
            )
            if new_client_div.is_displayed:
                status = None
                return (status, "", "", browser)
        except:
            logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao")
            
        next_button = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CT"]/span/button'))
        )
        next_button.click()
        browser.implicitly_wait(5)
        
        services_div = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        )
        services_div.click()
        browser.implicitly_wait(2)
        
        init_atend_button = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'INICIAR ATENDIMENTO')]"))
        )
        init_atend_button.click()
        browser.implicitly_wait(5)
        
        # //*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/span/a
        fatura_link = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='Fatura e segunda via']"))
        )
        fatura_link.click()
        browser.implicitly_wait(5)
        
        # Pegar as Informaçoes da div
        # status = "PAGA"
        # data = "01/07/2024"
        # valor = "R$ 1,00"
        
        status = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div'))
        )
        status = status.text
        browser.implicitly_wait(1)
        
        data = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]'))
        )
        data = data.text
        browser.implicitly_wait(1)
        
        valor = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/span/span'))
        )
        valor = valor.text
        browser.implicitly_wait(3)
        
        username = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
        )
        username.click()
        browser.implicitly_wait(3)
        
        return_select_screen = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
        )
        return_select_screen.click()
        browser.implicitly_wait(3)
        
        
        return (status, data, valor, browser)
    
    if tipo == 'VAREJO':
        seller_id = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, 'NOME_OPERADOR'))
        )
        seller_id.click()
        seller_id.send_keys("TR791422")
        
        seller_info = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, '//*[@id="po0"]'))
        )
        seller_info.click()
        browser.implicitly_wait(2)
        
        cnpj_input = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, 'AuxiliarCOD_IDENT_PESSOA'))
        )
        cnpj_input.click()
        cnpj_input.send_keys(documento)
        browser.implicitly_wait(1)
        
        cnpj_search_button = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CT"]/button'))
        )
        cnpj_search_button.click()
        browser.implicitly_wait(5)

        try:
            product_button = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="CT"]/div/div/div'))
            )
            if product_button.is_displayed:
                product_button.click()
                browser.implicitly_wait(5)
        except:
            logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao")
        try:
            new_client_div = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Novo Cliente')]"))
            )
            if new_client_div.is_displayed:
                status = None
                return (status, "", "", browser)
        except:
            logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao")

        next_button = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CT"]/span/button'))
        )
        next_button.click()
        browser.implicitly_wait(5)

        services_div = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        )
        services_div.click()
        browser.implicitly_wait(2)
        
        init_atend_button = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'INICIAR ATENDIMENTO')]"))
        )
        init_atend_button.click()
        browser.implicitly_wait(5)
        
        fatura_link = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='Fatura e segunda via']"))
        )
        fatura_link.click()
        browser.implicitly_wait(5)
        
        status = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div'))
        )
        status = status.text
        browser.implicitly_wait(1)
        
        data = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]'))
        )
        data = data.text
        browser.implicitly_wait(1)
        
        valor = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/span/span'))
        )
        valor = valor.text
        browser.implicitly_wait(1)
        
        # Pegar as Informaçoes da div
        # status = "PAGA"
        # data = "01/07/2024"
        # valor = "R$ 1,00"
        
        return (status, data, valor, browser)


def iniciar_atendimento(browser: webdriver.Chrome, documento: str, tipo: str, logging) :
    """
    Inicia a procura por documento no navegador
    
    Entrada:
        browser (WebDriver): instância do navegador do navegador aberto
        documento (str): o documento buscado
        tipo (str): se o cliente é EMPRESARIAL ou VAREJO

    Saída:
        tuple((VALOR, STATUS, DATA, BROWSER))
    """
    access_type_select = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, 'AcessoSelecionado'))
    )
    access_type_select.click()

    if tipo == 'EMPRESARIAL':
        emp_selected = access_type_select.find_element(By.XPATH, '//*[@id="AcessoSelecionado"]/option[3]')
        emp_selected.click()
        init_button = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.ID, 'PegaOnlyOnce'))
        )
        init_button.click()
        browser.implicitly_wait(5)
        result = search_doc(browser, documento, tipo, logging)
        
    if tipo == 'VAREJO':
        var_selected = access_type_select.find_element(By.XPATH, '//*[@id="AcessoSelecionado"]/option[2]')
        var_selected.click()
        init_button = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.ID, 'PegaOnlyOnce'))
        )
        init_button.click()
        browser.implicitly_wait(5)
        result = search_doc(browser, documento, tipo, logging)
        
    return result