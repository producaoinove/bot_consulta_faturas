from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

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
        opcoes.add_argument("window-size=1920,1080")
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

def search_doc(browser: webdriver.Chrome, documento: str, tipo: str, logging, actions: ActionChains):
    status = ""
    data = ""
    valor = ""
    documento = str(documento)
    tr = "TR791422"
    # browser.implicitly_wait(30)
    # time.sleep(10)
    # print("Saiu da pausa")

    browser.implicitly_wait(15)

    res = resposta_empresarial_busca(browser, documento, actions)

    browser = res[0]
    info_cliente = res[1]

        if info_cliente == "Novo Cliente":
            status = "Novo Cliente"
        elif info_cliente == "Nova Fibra":
            status = "Nova Fibra"

        # try:
        #     product_button = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'1-1')]"))
        #     )
        #     if product_button.is_displayed:
        #         actions.move_to_element(product_button).click().perform()
        #         browser.implicitly_wait(5)
        # except Exception as e:
        #     logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao: {e}")

        # try:
        #     new_client_div = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Novo Cliente')]"))
        #     )
        #     if new_client_div.is_displayed:
        #         print('Novo Cliente')
        #         browser.execute_script("window.history.go(-2)")
        #         time.sleep(5)
        #         # status = None
        #         # username = WebDriverWait(browser, 20).until(
        #         #     EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRUNA EMILY LEMOS DE MATTOS')]"))
        #         # )
        #         # try:
        #         #     username.click()
        #         # except:
        #         #     actions.move_to_element(username).click().perform()
        #         # print('Foi pro nome')
        #         # browser.implicitly_wait(3)
                
        #         # try:
        #         #     # return_select_screen = WebDriverWait(browser, 20).until(
        #         #     #     EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
        #         #     # )
        #         #     return_select_screen = WebDriverWait(browser, 20).until(
        #         #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Portal')]"))
        #         #     )
        #         # except:
        #         #     # return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        #         #     return_select_screen = username.find_element(By.XPATH, "//*[contains(text(), 'Portal')]")
                    
        #         # actions.move_to_element(return_select_screen).click().perform()
        #         # browser.execute_script("switchApplication('OiAuthentication')")
        #         # browser.implicitly_wait(3)
        #         print('Retornando pro menu')
        #         return (status, "", "", browser)
        # except Exception as e:
        #     logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao {e}")
            
        # browser.implicitly_wait(3)
        # next_button = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'AVANÇAR')]"))
        # )
        # next_button.click()
        # browser.implicitly_wait(5)
        
        # services_div = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        # )
        # services_div.click()
        # browser.implicitly_wait(10)
        
        # init_atend_button = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'INICIAR ATENDIMENTO')]"))
        # )
        # init_atend_button.click()
        # browser.implicitly_wait(10)
        
        # # //*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/span/a
        # fatura_link = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[text()='Fatura e segunda via']"))
        # )
        # fatura_link.click()
        # browser.implicitly_wait(10)
        
        # # Pegar as Informaçoes da div
        # # status = "PAGA"
        # # data = "01/07/2024"
        # # valor = "R$ 1,00"
        
        # status = browser.find_elements(By.XPATH, "//div[contains(text(), 'Pago') or contains(text(), 'Não Pago') or contains(text(), 'Vencido')]")
        
        # status = status[0].text
        # browser.implicitly_wait(1)
        
        # data = browser.find_elements(By.XPATH, "//*[contains(text(), '/')]")
        
        # data = data[0].text
        # browser.implicitly_wait(1)
        
        # valor = browser.find_elements(By.XPATH, "//*[contains(text(), '$')]")
        
        # valor = valor[0].text
        # browser.implicitly_wait(3)
        
        # username = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
        # )        
        # username.click()
        # browser.implicitly_wait(3)

        # try:
        #     return_select_screen = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
        #     )
        # except:
        #     return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        # actions.move_to_element(return_select_screen).click().perform()
        # browser.execute_script("switchApplication('OiAuthentication')")
        # browser.implicitly_wait(3)

        browser = retorna_selecao(browser)

    #     return (status, data, valor)
    
    # if tipo == 'VAREJO':
    #     browser.implicitly_wait(15)
        
    #     res = resposta_varejo_busca(browser, documento, actions)

    #     browser = res[0]
    #     info_cliente = res[1]

        if info_cliente == "Novo Cliente":
            status = "Novo Cliente"
        elif info_cliente == "Nova Fibra":
            status = "Nova Fibra"
        elif info_cliente == "Legado":
            status = "Legado"
            browser = escolher_produto(browser)
            str(input("Pressione Enter apos selecionar produto...."))
        # try:
        #     product_button = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'1-1')]"))
        #     )
        #     if product_button.is_displayed:
        #         actions.move_to_element(product_button).click().perform()
        #         browser.implicitly_wait(5)
        # except:
        #     logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao")
        # try:
        #     new_client_div = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Novo Cliente')]"))
        #     )
        #     if new_client_div.is_displayed:
        #         print('Novo Cliente')
        #         browser.execute_script("window.history.go(-1)")
        #         time.sleep(5)
        #         # status = None
        #         # username = WebDriverWait(browser, 20).until(
        #         #     EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRUNA EMILY LEMOS DE MATTOS')]"))
        #         # )
        #         # try:
        #         #     username.click()
        #         # except:
        #         #     actions.move_to_element(username).click().perform()
        #         # print('Foi pro nome')
        #         # browser.implicitly_wait(3)
                
        #         # try:
        #         #     # return_select_screen = WebDriverWait(browser, 20).until(
        #         #     #     EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
        #         #     # )
        #         #     return_select_screen = WebDriverWait(browser, 20).until(
        #         #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Portal')]"))
        #         #     )
        #         # except:
        #         #     # return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        #         #     return_select_screen = username.find_element(By.XPATH, "//*[contains(text(), 'Portal')]")
                    
        #         # actions.move_to_element(return_select_screen).click().perform()
        #         # browser.execute_script("switchApplication('OiAuthentication')")
        #         # browser.implicitly_wait(3)
                
        #         return (status, "", "", browser)
        # except:
        #     logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao")

        # next_button = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'AVANÇAR')]"))
        # )
        
        # next_button.click()
        # browser.implicitly_wait(5)

        # services_div = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        # )
        # actions.move_to_element(services_div).click().perform()
        # # services_div.click()
        # browser.implicitly_wait(2)
        
        # init_atend_button = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'INICIAR ATENDIMENTO')]"))
        # )
        # init_atend_button.click()
        # browser.implicitly_wait(5)
        
        # fatura_link = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Fatura e segunda via')]"))
        # )
        # fatura_link.click()
        # browser.implicitly_wait(5)
        
        # # Pegar as Informaçoes da div
        # # status = "PAGA"
        # # data = "01/07/2024"
        # # valor = "R$ 1,00"
        
        # status = browser.find_elements(By.XPATH, "//div[contains(text(), 'Pago') or contains(text(), 'Não Pago') or contains(text(), 'Vencido')]")
        
        # status = status[0].text
        # print(status)
        # browser.implicitly_wait(1)
        
        # data = browser.find_elements(By.XPATH, "//*[contains(text(), '/')]")
        
        # data = data[0].text
        # print(data)
        # browser.implicitly_wait(1)
        
        # valor = browser.find_elements(By.XPATH, "//*[contains(text(), '$')]")
        
        # valor = valor[0].text
        # print(valor)
        # browser.implicitly_wait(3)
        
        # username = WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
        # )
        # username.click()
        # browser.implicitly_wait(3)
        # try:
        #     return_select_screen = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
        #     )
        # except:
        #     return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        # actions.move_to_element(return_select_screen).click().perform()
        # browser.execute_script("switchApplication('OiAuthentication')")
        # browser.implicitly_wait(3)
        # browser.implicitly_wait(3)
        browser = retorna_selecao(browser)
        return (status, data, valor)

def retorna_selecao(browser):
    try:
        username = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[data-test-id="2017091914214003818486"]'))
        )
        username.click()
        WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.ID, 'ItemMiddle'))
        )
        actions = ActionChains(browser)
        return_select_screen = browser.find_element(By.ID, 'ItemMiddle')
        actions.move_to_element(return_select_screen).click().perform()
        browser.execute_script("switchApplication('OiAuthentication')")
    except Exception as e:
        print(f"Erro: {e}")

    return browser

def buscar_cliente(browser, documento, actions, tipo_busca):
    cnpj_input = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, 'AuxiliarCOD_IDENT_PESSOA'))
    )
    
    cnpj_input.send_keys(documento)
    data_change_value = cnpj_input.get_attribute('data-change')
    if data_change_value:
        browser.execute_script(data_change_value)

    cnpj_search_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Buscar')]"))
    )

    try:
        actions.move_to_element(cnpj_search_button).click().perform()
    except:
        cnpj_search_button = browser.find_element(By.NAME, f'PerformanceNovoAtendimentoBuscaCliente_pyDisplayHarness_{tipo_busca}')
        data_click_value = cnpj_search_button.get_attribute('data-click')
        if data_click_value:
            browser.execute_script(data_click_value)

    time.sleep(5)

    return browser

def verificar_cliente(driver):

    str(input('Pressione enter apos buscar o documento...'))

    script_span = '''
var xpath = "//span[text()='OITOTAL_FXBL']";
var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
var element = result.singleNodeValue;

if (element) {
    return "Legado";
} else {
    return null;
}
    '''
    result_span = driver.execute_script(script_span)

    if result_span:
        return (driver, 'Legado')

    script_div = '''
var xpath = "//div[contains(text(), 'Novo Cliente')]";
var result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
var numElements = result.snapshotLength;

for (var i = 0; i < numElements; i++) {
    var element = result.snapshotItem(i);
    return "Novo Cliente";
}

return null;
    '''
    result_div = driver.execute_script(script_div)

    if result_div:
        return (driver, 'Novo Cliente')

    return (driver, 'Nova Fibra')

def resposta_empresarial_busca(browser, documento, actions):
    browser = buscar_cliente(browser, documento, actions, tipo_busca='20')
    cliente = verificar_cliente(browser)
    browser = cliente[0]
    info_cliente = cliente[1]
    return (browser, info_cliente)

def resposta_varejo_busca(browser, documento, actions):
    browser = buscar_cliente(browser, documento, actions, tipo_busca='12')
    cliente = verificar_cliente(browser)
    browser = cliente[0]
    info_cliente = cliente[1]
    return (browser, info_cliente)

def escolher_produto(browser : webdriver.Chrome, tipo):

    try:
        produto_selector = '''
var xpath = "//span[text()='OITOTAL_FXBL']";
var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
var produtoElement = result.singleNodeValue;
if (produtoElement) {
    produtoElement.click();
    return "Produto encontrado e clicado";
} else {
    return "Produto não encontrado";
}
        '''
        resultado = browser.execute_script(produto_selector)
        
        if resultado == "Produto encontrado e clicado":
            avançar_button_selector = '''
        var xpath = "//button[contains(text(), 'AVANÇAR')]";
        var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        var buttonElement = result.singleNodeValue;
        buttonElement.click();
            '''
            browser.execute_script(avançar_button_selector)

            print("produto selecionado e pagina avançada")

        else:
            print("Erro ao selecionar o produto:", resultado)

    except Exception as e:
        print(f"Erro: {e}")

    return browser

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
    
    
    # access_type_select = WebDriverWait(browser, 20).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="AcessoSelecionado"]'))
    # )
    access_type_select = Select(browser.find_element(By.XPATH, '//*[@id="AcessoSelecionado"]'))
    emp_select = 'Oi360Empresarial'
    var_select = 'Oi360Varejo'
    
    init_button = browser.find_element(By.XPATH, "//button[contains(text(), 'INICIAR')]")
    
    if tipo == 'EMPRESARIAL':
        access_type_select.select_by_visible_text(emp_select)
        browser.implicitly_wait(5)
        actions = ActionChains(browser)
        actions.move_to_element(init_button).click().perform()
        browser.implicitly_wait(1)
        browser.execute_script('switchApplication("#~OperatorID.AcessoSelecionado~#")')
        browser.implicitly_wait(5)
        str(input("Pressione enter apos selecionar empresarial..."))
        result = search_doc(browser, documento, tipo, logging, actions)
        
    if tipo == 'VAREJO':
        access_type_select.select_by_visible_text(var_select)
        browser.implicitly_wait(5)
        actions = ActionChains(browser)
        actions.move_to_element(init_button).click().perform()
        browser.implicitly_wait(1)
        browser.execute_script('switchApplication("#~OperatorID.AcessoSelecionado~#")')
        browser.implicitly_wait(5)
        str(input("Pressione enter apos selecionar varejo..."))
        result = search_doc(browser, documento, tipo, logging, actions)
    return result
