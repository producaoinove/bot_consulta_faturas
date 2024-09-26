import os

raiz = os.path.dirname(os.getcwd())

path_codigo = os.path.join(raiz, 'src')
path_entrada = os.path.join(raiz, 'db')
path_saida = os.path.join(raiz, 'out')
path_log = os.path.join(raiz, 'log')
path_temporario = os.path.join(raiz, 'temp')
path_testes = os.path.join(raiz, 'tests')
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

if __name__ == "__main__":

    arquivo_input = os.path.join(path_entrada, "controle_qualidade.xlsx")
    planilha_input = "Safras em Tratamento"
    arquivo_output = os.path.join(path_saida, "relatorio.csv")

    df = ler_controle_qualidade(path_file=arquivo_input, planilha=planilha_input)
    df = tratar_controle_qualidade(df)
    print(df)

