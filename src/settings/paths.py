import os

# raiz = "C:\\Users\\Optiplex_3050\\Documents\\producao_inove\\bot_consulta_faturas"
raiz = os.path.dirname(os.getcwd())

path_codigo = os.path.join(raiz, 'src')
path_entrada = os.path.join(raiz, 'fonts')
path_saida = os.path.join(raiz, 'out')
path_log = os.path.join(raiz, 'log')
path_temporario = os.path.join(raiz, 'temp')
path_testes = os.path.join(raiz, 'tests')
