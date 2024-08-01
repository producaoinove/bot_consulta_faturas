from .gerais import main
from .dataframes import ler_controle_qualidade, tratar_controle_qualidade, exportar_controle_qualidade
from .navegador import criar_navegador, realizar_login, iniciar_atendimento, search_doc, escolher_tipo_cliente

__all__ = [
    'criar_navegador',
    'iniciar_atendimento',
    'search_doc',
    'escolher_tipo_cliente',
    'realizar_login',
    'ler_controle_qualidade',
    'tratar_controle_qualidade',
    'exportar_controle_qualidade',
    'main'
]
