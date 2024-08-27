from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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

def search_doc(browser: webdriver.Chrome, documento: str, tipo: str, logging, actions: ActionChains):
    status = ""
    documento = str(documento)
    tr = "TR791422"
    browser.implicitly_wait(5)

    if tipo == 'EMPRESARIAL':
        cnpj_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, 'AuxiliarCOD_IDENT_PESSOA'))
        )
        cnpj_input.send_keys(documento)
        browser.implicitly_wait(3)
        
        cnpj_search_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Buscar')]"))
        ) # VER SE TEM ALGUMA FUNÇAO PRA RODAR NO JS
        actions.move_to_element(cnpj_search_button).click().perform()
        # cnpj_search_button.click()
        
        # cnpj_search_button = browser.find_element(By.NAME, 'PerformanceNovoAtendimentoBuscaCliente_pyDisplayHarness_12')
        # data_click_value = button.get_attribute('data-click')
        # driver.execute_script(data_click_value)
        
        
        browser.implicitly_wait(10)
        
        try:
            product_button = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'1-1')]"))
            )
            if product_button.is_displayed:
                actions.move_to_element(product_button).click().perform()
                browser.implicitly_wait(5)
        except Exception as e:
            logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao: {e}")

        try:
            new_client_div = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Novo Cliente')]"))
            )
            if new_client_div.is_displayed:
                status = None
                username = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
                )
                username.click()
                browser.implicitly_wait(3)
                
                try:
                    return_select_screen = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
                    )
                except:
                    return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
                actions.move_to_element(return_select_screen).click().perform()
                browser.execute_script("switchApplication('OiAuthentication')")
                browser.implicitly_wait(3)
                return (status, "", "", browser)
        except Exception as e:
            logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao {e}")
            
        browser.implicitly_wait(3)
        next_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'AVANÇAR')]"))
        )
        next_button.click()
        browser.implicitly_wait(15)
        
        services_div = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        )
        services_div.click()
        browser.implicitly_wait(10)
        
        init_atend_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'INICIAR ATENDIMENTO')]"))
        )
        init_atend_button.click()
        browser.implicitly_wait(10)
        
        # //*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/span/a
        fatura_link = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Fatura e segunda via']"))
        )
        fatura_link.click()
        browser.implicitly_wait(10)
        
        # Pegar as Informaçoes da div
        # status = "PAGA"
        # data = "01/07/2024"
        # valor = "R$ 1,00"
        
        status = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Pago') or contains(text(), 'Não Pago') or contains(text(), 'Vencido')]"))
        )
        status = status[0].text
        browser.implicitly_wait(1)
        
        data = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '/')]"))
        )
        data = data[0].text
        browser.implicitly_wait(1)
        
        valor = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '$')]"))
        )
        valor = valor[0].text
        browser.implicitly_wait(3)
        
        username = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
        )
        username.click()
        browser.implicitly_wait(3)

        try:
            return_select_screen = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
            )
        except:
            return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        actions.move_to_element(return_select_screen).click().perform()
        browser.execute_script("switchApplication('OiAuthentication')")
        browser.implicitly_wait(3)
        
        
        return (status, data, valor, browser)
    
    if tipo == 'VAREJO':
        
        seller_id = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, 'NOME_OPERADOR'))
        )
        seller_id.send_keys(tr)
        browser.implicitly_wait(15)
        actions.key_down(Keys.TAB)
        browser.implicitly_wait(15)
        # seller_info = WebDriverWait(browser, 5).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'LUIZ EDUARDO PONTES ESQUIVEL')]"))
        # )

        # if seller_info.is_displayed():
        #     actions.move_to_element(seller_info).click().perform()
        #     browser.implicitly_wait(5)

        # try:
        #     browser.execute_script("document.activeElement.blur();")
        # except:
        #     print("Erro ao tentar desfocar elemento")
        #     body = browser.find_element(By.TAG_NAME, "body")
        #     actions.move_to_element(body).click().perform()

        # seller_info.click()
        
        # body = browser.find_element(By.TAG_NAME, "body")
        # actions.move_to_element(body).click().perform()
        # browser.implicitly_wait(5)
        # actions.reset_actions()
        
        
        cnpj_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, 'AuxiliarCOD_IDENT_PESSOA'))
        )
        # browser.execute_script("arguments[0].value = arguments[1];", cnpj_input, documento)
        # actions.send_keys_to_element(cnpj_input, documento)
        cnpj_input.send_keys(documento)

        print(cnpj_input.get_attribute('value'))
        browser.implicitly_wait(1)

        cnpj_search_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Buscar')]"))
        ) # VER SE TEM ALGUMA FUNÇAO PRA RODAR NO JS
        
        try:
            actions.move_to_element(cnpj_search_button).click().perform()
        except:
            cnpj_search_button = browser.find_element(By.NAME, 'PerformanceNovoAtendimentoBuscaCliente_pyDisplayHarness_12')
            data_click_value = cnpj_search_button.get_attribute('data-click')
            browser.execute_script(data_click_value)
            # cnpj_search_button.click()

        # cnpj_search_button = browser.find_element(By.NAME, 'PerformanceNovoAtendimentoBuscaCliente_pyDisplayHarness_12')
        # data_click_value = button.get_attribute('data-click')
        # driver.execute_script(data_click_value)

        browser.implicitly_wait(15)

        try:
            product_button = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'1-1')]"))
            )
            if product_button.is_displayed:
                actions.move_to_element(product_button).click().perform()
                browser.implicitly_wait(5)
        except:
            logging.error(f"Botão produto nao encontrado, seguindo fluxo da execucao")
        try:
            new_client_div = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Novo Cliente')]"))
            )
            if new_client_div.is_displayed:
                status = None
                username = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
                )
                username.click()
                browser.implicitly_wait(3)
                try:
                    return_select_screen = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
                    )
                except:
                    return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
                actions.move_to_element(return_select_screen).click().perform()
                browser.execute_script("switchApplication('OiAuthentication')")
                browser.implicitly_wait(3)
                
                return (status, "", "", browser)
        except:
            logging.error(f"Div Novo Cliente nao encontrada, seguindo fluxo da execucao")

        next_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'AVANÇAR')]"))
        )
        next_button.click()
        browser.implicitly_wait(5)

        services_div = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div'))
        )
        actions.move_to_element(services_div).click().perform()
        # services_div.click()
        browser.implicitly_wait(2)
        
        init_atend_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'INICIAR ATENDIMENTO')]"))
        )
        init_atend_button.click()
        browser.implicitly_wait(5)
        
        fatura_link = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Fatura e segunda via')]"))
        )
        fatura_link.click()
        browser.implicitly_wait(5)
        
        # Pegar as Informaçoes da div
        # status = "PAGA"
        # data = "01/07/2024"
        # valor = "R$ 1,00"
        
        status = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Pago') or contains(text(), 'Não Pago') or contains(text(), 'Vencido')]"))
        )
        status = status[0].text
        print(status)
        browser.implicitly_wait(1)
        
        data = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '/')]"))
        )
        data = data[0].text
        print(data)
        browser.implicitly_wait(1)
        
        valor = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '$')]"))
        )
        valor = valor[0].text
        print(valor)
        browser.implicitly_wait(3)
        
        username = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="RULE_KEY"]/div/div/div/div/div/div/div/div/div[2]/span/a'))
        )
        username.click()
        browser.implicitly_wait(3)
        try:
            return_select_screen = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ItemMiddle"]'))
            )
        except:
            return_select_screen = username.find_element(By.XPATH, '//*[@id="ItemMiddle"]')
        actions.move_to_element(return_select_screen).click().perform()
        browser.execute_script("switchApplication('OiAuthentication')")
        browser.implicitly_wait(3)
        browser.implicitly_wait(3)
        
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
    
    
    # access_type_select = WebDriverWait(browser, 5).until(
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
        result = search_doc(browser, documento, tipo, logging, actions)
        
    if tipo == 'VAREJO':
        access_type_select.select_by_visible_text(var_select)
        browser.implicitly_wait(5)
        actions = ActionChains(browser)
        actions.move_to_element(init_button).click().perform()
        browser.implicitly_wait(1)
        browser.execute_script('switchApplication("#~OperatorID.AcessoSelecionado~#")')
        result = search_doc(browser, documento, tipo, logging, actions)

    return result