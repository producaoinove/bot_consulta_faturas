import os
import pandas as pd
from selenium import webdriver

def coletar_informacoes(documento: str, tipo: str, mes_safra: str, browser : webdriver.Chrome, logging) -> tuple:
    """
    Recebe um documento (CNPJ ou CPF) e retorna os dados exigidos (VALOR; STATUS; DATA)

    Entrada:
        documento (str): o documento que serão buscados
        tipo_pessoa (str): se o cliente é CPF | MEI | NMEI
        mes_safra (str): qual o mes da safra em questão

    Saída:
        Uma tupla com os três dados (VALOR, STATUS, DATA)

    """
    from modules.navegador import iniciar_atendimento

    if 'CPF' in tipo.upper():
        tipo_p = "VAREJO"
        atendimento = iniciar_atendimento(browser, documento, tipo_p, mes_safra, logging)
        status = atendimento[0]
        data = atendimento[1]
        valor = atendimento[2]
        # print('Skip Varejo')
        if status == "Novo Cliente":
            status = "NOVO CLIENTE"
            valor = ""
            data = ""
        if status == "Nova Fibra":
            status = "NOVO CLIENTE"
            valor = ""
            data = ""
        # status = "TESTE"
        # valor = "TESTE"
        # data = "TESTE"
    elif 'MEI' in tipo.upper() or 'EMP' in tipo.upper():
        tipo_p = "EMPRESARIAL"
        atendimento = iniciar_atendimento(browser, documento, tipo_p, mes_safra, logging)
        status = atendimento[0]
        data = atendimento[1]
        valor = atendimento[2]
        if status == "Novo Cliente":
            status = "NOVO CLIENTE"
            valor = ""
            data = ""
        if status == "Nova Fibra":
            status = "NOVO CLIENTE"
            valor = ""
            data = ""
    else:
        raise Exception("O tipo_pessoa passado é inválido!")

    # try:
    #     valor = "R$ 50,00"
    #     status = "PENDENTE"
    #     data = "24/07/2024"
    # except:
    #     valor, status, data = None, None, None

    return (valor, status, data)

def main(logging):
    """
    Raíz do código fonte
    """

    from settings import path_entrada, path_saida, setup_log, path_log
    from modules import ler_controle_qualidade, tratar_controle_qualidade, exportar_controle_qualidade, criar_navegador, realizar_login

    setup_log('bot_consulta_faturas', path_log)

    browser = criar_navegador()
    print("Navegador criado!")

    realizar_login(browser, 'https://oi360.oi.net.br/prweb/PRServletCustom/AX6P2laLe91D09R0jTjfNJdv0u0s3qcA*/!STANDARD?pyActivity=Data-Portal.ShowDesktop#!')
    print("Login realizado!")

    arquivo_input = os.path.join(path_entrada, "controle_qualidade.xlsx")
    planilha_input = "Safras em Tratamento"
    arquivo_output = os.path.join(path_saida, "relatorio.csv")
    arquivo_error_out = os.path.join(path_saida, "relatorio_com_erros.csv")

    df = ler_controle_qualidade(arquivo_input, planilha_input)
    total_inicial = len(df)
    df = tratar_controle_qualidade(df)
    dados_extraidos = []
    print("Arquivo xlsx lido e dados extraidos")

    for index, linhas in df.iterrows():
        if index != 0:
            print("----------------------------------------------------------------------------------------")
        doc = linhas['DOC']
        tipo_p = linhas['TIPO_CLIENTE']
        mes_safra = linhas['MES_SAFRA']
        print(doc, tipo_p, mes_safra)
        try:
            valor, status, data = coletar_informacoes(doc, tipo_p, mes_safra, browser, logging)
            if valor == '' and status == '' and data == '':
                dados_extraidos.append(('R$0,00', 'ERRO DE LEITURA', 'ERRO'))
            else:
                dados_extraidos.append((valor, status, data))
            print(valor, status, data)
        except:
            logging.error(f"Erro de leitura, documento {doc}")
            status = "ERRO DE LEITURA"
            dados_extraidos.append(("R$0,00", status, "ERRO"))

    if ('', '', '') in dados_extraidos:
        dados_extraidos.remove(('', '', ''))

    df[['VALOR', 'STATUS', 'DATA']] = pd.DataFrame(dados_extraidos, index = df.index)
    df = df[['DOC', 'VALOR', 'STATUS', 'DATA']]
    try:
        df_error = df[df['STATUS'] == 'ERRO DE LEITURA']
        exportar_controle_qualidade(df_error, arquivo_error_out)
    except Exception as e:
        logging.error(f"Erro na criação do arquivo de relatório com os erros, Detalhes: {e}")
    df = df[df['STATUS'] != 'ERRO DE LEITURA']
    res =  exportar_controle_qualidade(df, arquivo_output)

    if res == "SUCESSO":
        total_buscados = len(df)
        total_validados = df['VALOR'].notna().sum()
        total_nao_validados = df['VALOR'].isna().sum()

        return total_inicial, total_buscados, total_validados, total_nao_validados
    return None