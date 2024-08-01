import os
import pandas as pd

def coletar_informacoes(documento: str, tipo_pessoa: str) -> tuple:
    """
Recebe um documento (CNPJ ou CPF) e retorna os dados exigidos (VALOR; STATUS; DATA)

Entrada:
    documento (str): o documento que serão buscados
    tipo_pessoa (str): se o cliente é CPF | MEI | NMEI

Saída:
    Uma tupla com os três dados (VALOR, STATUS, DATA)

    """

    if 'CPF' in tipo_pessoa.upper():
        tipo_p = "VAREJO"
    elif 'MEI' in tipo_pessoa.upper() or 'EMP' in tipo_pessoa.upper():
        tipo_p = "EMPRESARIAL"
    else:
        raise Exception("O tipo_pessoa passado é inválido!")

    try:
        valor = "R$ 50,00"
        status = "PENDENTE"
        data = "24/07/2024"
    except:
        valor, status, data = None, None, None

    return (valor, status, data)

def main():
    """
Raíz do código fonte
    """

    from settings import path_entrada, path_saida, setup_log, path_log
    from modules import ler_controle_qualidade, tratar_controle_qualidade, exportar_controle_qualidade, criar_navegador, realizar_login

    setup_log('bot_consulta_faturas', path_log)

    browser = criar_navegador()
    realizar_login(browser, 'https://oi360.oi.net.br/prweb/PRServletCustom/AX6P2laLe91D09R0jTjfNJdv0u0s3qcA*/!STANDARD?pyActivity=Data-Portal.ShowDesktop#!')

    arquivo_input = os.path.join(path_entrada, "controle_qualidade.xlsx")
    planilha_input = "Safras em Tratamento"

    arquivo_output = os.path.join(path_saida, "relatorio.csv")

    df = ler_controle_qualidade(arquivo_input, planilha_input)
    total_inicial = len(df)
    df = tratar_controle_qualidade(df)
    dados_extraidos = []
    for _, linhas in df.iterrows():
        doc = linhas['DOC']
        tipo_p = linhas['TIPO_CLIENTE']
        valor, status, data = coletar_informacoes(doc, tipo_p)
        dados_extraidos.append((valor, status, data))
    df[['VALOR', 'STATUS', 'DATA']] = pd.DataFrame(dados_extraidos, index=df.index)
    df = df[['DOC', 'VALOR', 'STATUS', 'DATA']]
    res =  exportar_controle_qualidade(df, arquivo_output)
    if res == "SUCESSO":

        total_buscados = len(df)
        total_validados = df['VALOR'].notna().sum()
        total_nao_validados = df['VALOR'].isna().sum()

        return total_inicial, total_buscados, total_validados, total_nao_validados
    return None