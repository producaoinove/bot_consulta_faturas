import pandas as pd

dict_info360 = {}

def process_fatura_data(fatura_data: dict, mes_safra: str):
    try:
        lista_datas = fatura_data['datas']
        lista_valores = fatura_data['valores']
        lista_status = fatura_data['status']
        print("Listas iniciais:")
        print(f"Datas: {lista_datas}")
        print(f"Valores: {lista_valores}")
        print(f"Status: {lista_status}")
        indice_atual = 0
        while indice_atual < len(lista_datas) - 1:
            print(f"\nAnalisando índice {indice_atual}:")
            print(f"Data: {lista_datas[indice_atual]}, Status: {lista_status[indice_atual]}")
            if lista_status[indice_atual] == 'pago':
                print(f"Removendo data para status pago {indice_atual + 1}")
                del lista_datas[indice_atual + 1]
                indice_atual += 1
            else:
                indice_atual += 1
            print(f"Listas após remoção (se houver):")
            print(f"Datas: {lista_datas}")
            print(f"Valores: {lista_valores}")
            print(f"Status: {lista_status}")
        safra_indices = [idx for idx, data in enumerate(lista_datas) if pd.to_datetime(data, format='%d/%m/%Y').month == int(mes_safra)]
        resultado_final = {
            'datas': [lista_datas[idx] for idx in safra_indices],
            'valores': [lista_valores[idx] for idx in safra_indices],
            'status': [lista_status[idx] for idx in safra_indices]
        }
        print("Valores: ", resultado_final['valores'])
        print("Datas: ", resultado_final['datas'])
        print("Status: ", resultado_final['status'])
        return resultado_final

    except Exception as e:
        print(f"Falha ao processar as informações das faturas, detalhes: {str(e)}")
        return None

if __name__ == "__main__":
    print("Deu certo!")
    dados_simulados = {
        'datas': ['11/09/2024', '12/08/2024', '12/08/2024', '15/07/2024', '05/07/2024'],
        'valores': ['R$110,06', 'R$109,80', 'R$77,90'],
        'status': ['em aberto', 'pago', 'pago']
    }
    process_fatura_data(dados_simulados, '7')