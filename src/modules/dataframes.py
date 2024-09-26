import pandas as pd


def construir_coluna_aux(tipo):
    tipo = str(tipo)
    if tipo == 'NMEI' or tipo == 'MEI':
        return 'EMPRESARIAL'
    else:
        return 'VAREJO'

def ler_controle_qualidade(path_file: str, planilha: str) -> pd.DataFrame:
    """
Ler o arquivo do Back-Office (Controle de qualidade)

Entrada:
    path_file (str): o caminho do arquivo fonte
    planilha (str): a planilha a ser considerada pelo tratamento

Saída:
    DataFrame do pandas com conteúdo do arquivo
    """
    ler_arquivo = pd.read_excel(path_file, sheet_name=[planilha], skiprows=1, dtype=str)
    df = ler_arquivo[planilha]
    df = df.fillna('')
    return df

def tratar_controle_qualidade(df: pd.DataFrame) -> pd.DataFrame:
    """
Trata os dados conforme necessidade, para extrair o necessário.

Entrada:
    df (pd.DataFrame): o dataframe principal

Saída:
    DataFrame com dados defidamente tratados
    """

def tratar_controle_qualidade(df: pd.DataFrame) -> pd.DataFrame:
    """
Trata os dados conforme necessidade, para extrair o necessário.

Entrada:
    df (pd.DataFrame): o dataframe principal

Saída:
    DataFrame com dados defidamente tratados
    """

    if not isinstance(df, pd.DataFrame):
        raise Exception("Opa... parametro da função 'df' foi passado errado. df")

    df_tratado = df.copy()
    df_tratado = df_tratado[['CNPJChave', 'UNIDADE', 'Sistema OI', 'Safra']]
    df_tratado.rename(columns={'CNPJChave': 'DOC', 'UNIDADE': 'TIPO_CLIENTE'}, inplace=True)
    df_tratado = df_tratado[df_tratado['Sistema OI'] == "NO LEGADO"]
    df_tratado.drop(columns=['Sistema OI'])
    df_tratado['MES_SAFRA'] = pd.to_datetime(df_tratado['Safra'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df_tratado['MES_SAFRA'] = df_tratado['MES_SAFRA'].dt.month.astype(str).apply(lambda x: str(int(x) + 1))
    
    df_tratado = df_tratado[df_tratado['TIPO_CLIENTE'].isin(['CPF', 'MEI', 'NMEI'])]

    df_cpf = df_tratado[df_tratado['TIPO_CLIENTE'] == 'CPF']
    df_mei = df_tratado[df_tratado['TIPO_CLIENTE'] == 'MEI']
    df_nmei = df_tratado[df_tratado['TIPO_CLIENTE'] == 'NMEI']

    df_cpf = df_cpf.reset_index(drop=True)
    df_mei = df_mei.reset_index(drop=True)
    df_nmei = df_nmei.reset_index(drop=True)

    df_intercalado = pd.concat([df_cpf, df_mei, df_nmei], axis=1).stack().reset_index(drop=True)

    df_intercalado = pd.DataFrame(df_intercalado.values.reshape(-1, len(df_tratado.columns)), columns=df_tratado.columns)

    return df_intercalado

def exportar_controle_qualidade(df: pd.DataFrame, path_file: str) -> str:
    """
Exporta os dados tratados em um arquivo '.csv' na pasta 'out' com nome 'relatorio.csv'

Entrada:
    path_file (str): o caminho do arquivo fonte
    df (pd.DataFrame): o dataframe principal

Saída:
    String reprentando se houve sucesso
    """

    if not isinstance(df, pd.DataFrame):
        raise Exception("Opa... parametro da função 'exportar_csv' foi passado errado. df")

    try:
        df.to_csv(path_file, sep=';', index=False)
        return "SUCESSO"
    except Exception as e:
        raise Exception(f"Deu erro ao exportar o csv. Detalhes: {str(e)}")
