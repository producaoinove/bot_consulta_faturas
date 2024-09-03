required_packages = [
    "pandas",
    "datetime",
    "selenium",
]
from settings import verificar_pacotes, setup_log, path_log
from modules import main
import logging 

if __name__ == "__main__":

    try:
        verificar_pacotes(required_packages)
    except Exception as e:
        print(f"Falha ao verificar e baixar pacotes externos! Detalhes: {str(e)}")

    try:
        setup_log('bot_consulta_faturas', path_log)
    except Exception as e:
        print(f"Falha ao configurar arquivo de log! Detalhes: {str(e)}")

    try:
        logging.info("Bot iniciado!")
        res = main(logging)
        if res == None:
            logging.error("Erro nao fatal, na execucao do bot!")
        else:
            inicial = res[0]
            buscados = res[1]
            validado = res[2]
            nao_validado = res[3]

            logging.info(f'Total de registros inicial: {inicial}')
            logging.info(f'Total de registros buscados: {buscados}')
            logging.info(f'Total de registros validados: {validado}')
            logging.info(f'Total de registros nao validados: {nao_validado}')

        logging.info("Bot finalizado!")
    except Exception as e:
        logging.error(f"Deu erro no bot. Detalhes: {str(e)}")