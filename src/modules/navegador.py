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
    if tipo == 'EMPRESARIAL':
        browser.implicitly_wait(15)

        res = resposta_empresarial_busca(browser, documento, actions)

        browser = res[0]
        info_cliente = res[1]

    if info_cliente == "Novo Cliente":
        status = "Novo Cliente"
    elif info_cliente == "Nova Fibra":
        status = "Nova Fibra"
    elif info_cliente == "Legado":
        status = "Legado"
        browser = escolher_produto(browser, tipo)
        str(input("Pressione Enter apos selecionar produto...."))

        browser = retorna_selecao(browser)

        return (status, data, valor)
    
    if tipo == 'VAREJO':
        browser.implicitly_wait(15)
        
        res = resposta_varejo_busca(browser, documento, actions)

        browser = res[0]
        info_cliente = res[1]

        if info_cliente == "Novo Cliente":
            status = "Novo Cliente"
        elif info_cliente == "Nova Fibra":
            status = "Nova Fibra"
        elif info_cliente == "Legado":
            status = "Legado"
            browser = escolher_produto(browser)
            str(input("Pressione Enter apos selecionar produto...."))
            browser = escolher_servico(browser)
            str(input("Pressione Enter apos selecionar o serviço...."))

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

def escolher_produto(browser):

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

            actions = ActionChains(browser)

            if tipo == "VAREJO":
                elemento_avancar = browser.find_element(By.NAME, 'MainNovoAtendimento_pyDisplayHarness_60')
                data_click_value = elemento_avancar.get_attribute('data-click')
                actions.move_to_element(elemento_avancar).click().perform()
                print(data_click_value)
                if data_click_value:
                    browser.execute_script(data_click_value)
            elif tipo == "EMPRESARIAL":
                elemento_avancar = browser.find_element(By.NAME, 'MainNovoAtendimento_pyDisplayHarness_82')
                data_click_value = elemento_avancar.get_attribute('data-click')
                actions.move_to_element(elemento_avancar).click().perform()
                print(data_click_value)
                if data_click_value:
                    browser.execute_script(data_click_value)
            else:
                raise Exception("Tipo invalido de cliente")


            print("produto selecionado e pagina avançada")

        else:
            print("Erro ao selecionar o produto:", resultado)

    except Exception as e:
        print(f"Erro: {e}")

    return browser

def ir_segundavia(browser : webdriver.Chrome):
    fatura_link = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Fatura e segunda via']"))
    )
    fatura_link.click()
    browser.implicitly_wait(10)
    return browser

def get_fatura_infos(browser : webdriver.Chrome):
    print('teste')
    
    
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