import fundamentus
import psycopg2
from datetime import datetime
import numpy as np
    
def get_valor(df, campo, default=None):
    valor = df.get(campo, [default])[0]
    
    if isinstance(valor, str) and '%' in valor:
        # Remove o símbolo '%' e converte para float, se for um valor percentual
        valor = valor.replace('%', '')
        try:
            valor = float(valor)
        except ValueError:
            return default
    elif valor == '-':
        return default
    
    # Verifica se o valor é um tipo numpy (int64 ou float64) e converte para um tipo nativo do Python
    if isinstance(valor, (np.int64, np.float64)):
        return valor.item()  # Converte para int ou float nativo
    
    return valor

# Função para inserir dados na tabela 'acoes' se não existir
def inserir_acao(ticker, nome_empresa, setor, tipo):
    print((ticker, nome_empresa, setor, tipo ))

# Função para inserir os dados de indicadores no banco de dados
def inserir_indicadores(tickers):
        # Iterar sobre os tickers fornecidos
        for ticker in tickers:
            df = fundamentus.get_papel(ticker)
            
            # Extrair dados da ação
            nome_empresa = df['Empresa'].iloc[0]
            setor = df['Setor'].iloc[0]
            tipo = df['Tipo'].iloc[0]
            
            # Verificar e inserir a ação na tabela 'acoes', caso não exista
            acao_id = inserir_acao(ticker, nome_empresa, setor, tipo)

            cotacao = get_valor(df, 'Cotacao')
            pl = get_valor(df, 'PL')
            pvp = get_valor(df, 'PVP')
            div_yield = get_valor(df, 'Div_Yield')
            lpa = get_valor(df, 'LPA')
            vpa = get_valor(df, 'VPA')
            margem_ebit = get_valor(df, 'Marg_EBIT')
            margem_liquida = get_valor(df, 'Marg_Liquida')
            roe = get_valor(df, 'ROE')
            roic = get_valor(df, 'ROIC')
            liquidez_corrente = get_valor(df, 'Liquidez_Corr')
            div_bruta_patrim = get_valor(df, 'Div_Br_Patrim')
            cres_rec_5a = get_valor(df, 'Cres_Rec_5a')
            ev_ebitda = get_valor(df, 'EV_EBITDA')
            ev_ebit = get_valor(df, 'EV_EBIT')
            psr = get_valor(df, 'PSR')
            giro_ativos = get_valor(df, 'Giro_Ativos')
            receita_liquida_12m = get_valor(df, 'Receita_Liquida_12m')
            ebit_12m = get_valor(df, 'EBIT_12m')
            lucro_liquido_12m = get_valor(df, 'Lucro_Liquido_12m')
            receita_liquida_3m = get_valor(df, 'Receita_Liquida_3m')
            ebit_3m = get_valor(df, 'EBIT_3m')
            lucro_liquido_3m = get_valor(df, 'Lucro_Liquido_3m')
            data_ultima_cotacao = get_valor(df, 'Data_ult_cot')
            min_52_sem = get_valor(df, 'Min_52_sem')
            max_52_sem = get_valor(df, 'Max_52_sem')
            vol_med_2m = get_valor(df, 'Vol_med_2m')
            valor_de_mercado = get_valor(df, 'Valor_de_mercado')
            valor_da_firma = get_valor(df, 'Valor_da_firma')
            ult_balanco_processado = get_valor(df, 'Ult_balanco_processado')
            nro_acoes = get_valor(df, 'Nro_Acoes')
            pebit = get_valor(df, 'PEBIT')
            pativos = get_valor(df, 'PAtivos')
            pcap_giro = get_valor(df, 'PCap_Giro')
            pativ_circ_liq = get_valor(df, 'PAtiv_Circ_Liq')
            margem_bruta = get_valor(df, 'Marg_Bruta')
            ebit_ativo = get_valor(df, 'EBIT_Ativo')
            ativo = get_valor(df, 'Ativo')
            disponibilidades = get_valor(df, 'Disponibilidades')
            ativo_circulante = get_valor(df, 'Ativo_Circulante')
            divida_bruta = get_valor(df, 'Div_Bruta')
            divida_liquida = get_valor(df, 'Div_Liquida')
            data_atualizacao = datetime.now().date()
            patrim_liq = get_valor(df, 'Patrim_Liq')
            credito = get_valor(df, 'Cart_de_Credito')
            depositos = get_valor(df, 'Depositos')
            result_inter_financ_12m = get_valor(df, 'Result_Int_Financ_12m')
            receita_servicos_12m = get_valor(df, 'Rec_Servicos_12m')
            result_inter_financ_3m = get_valor(df, 'Result_Int_Financ_3m')
            receita_servicos_3m = get_valor(df, 'Rec_Servicos_3m')

            # Comando SQL para inserção dos dados de indicadores
            query = """
                INSERT INTO public.indicadores
                (
                    acao_id, credito, depositos, result_inter_financ_12m, receita_servicos_12m, result_inter_financ_3m, 
                    receita_servicos_3m, disponibilidades, ativo_circulante, divida_bruta, divida_liquida, 
                    receita_liquida_12m, ebit_12m, receita_liquida_3m, ebit_3m, cotacao, min_52_sem, max_52_sem, 
                    vol_med_2m, valor_de_mercado, valor_da_firma, ult_balanco_processado, nro_acoes, pl, pvp, pebit, psr, 
                    pativos, pcap_giro, pativ_circ_liq, div_yield, ev_ebitda, ev_ebit, cres_rec_5a, lpa, vpa, margem_bruta, 
                    margem_ebit, margem_liquida, ebit_ativo, roic, roe, liquidez_corrente, div_bruta_patrim, giro_ativos, 
                    ativo, lucro_liquido_12m, lucro_liquido_3m, patrim_liq, data_ultima_cotacao, data_atualizacao
                )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Inserir os dados de indicadores no banco de dados
            print(
                    acao_id, 
                    credito, 
                    depositos, 
                    result_inter_financ_12m, 
                    receita_servicos_12m, 
                    result_inter_financ_3m, 
                    receita_servicos_3m, 
                    disponibilidades, 
                    ativo_circulante, 
                    divida_bruta, 
                    divida_liquida, 
                    receita_liquida_12m, 
                    ebit_12m, 
                    receita_liquida_3m, 
                    ebit_3m, 
                    cotacao, 
                    min_52_sem, 
                    max_52_sem, 
                    vol_med_2m, 
                    valor_de_mercado, 
                    valor_da_firma, 
                    ult_balanco_processado, 
                    nro_acoes, 
                    pl, 
                    pvp, 
                    pebit, 
                    psr, 
                    pativos, 
                    pcap_giro, 
                    pativ_circ_liq, 
                    div_yield, 
                    ev_ebitda, 
                    ev_ebit, 
                    cres_rec_5a, 
                    lpa, 
                    vpa, 
                    margem_bruta, 
                    margem_ebit, 
                    margem_liquida, 
                    ebit_ativo, 
                    roic, 
                    roe, 
                    liquidez_corrente, 
                    div_bruta_patrim, 
                    giro_ativos, 
                    ativo, 
                    lucro_liquido_12m, 
                    lucro_liquido_3m, 
                    patrim_liq, 
                    data_ultima_cotacao, 
                    data_atualizacao
            )

# Função principal
def main():
    # Conectar ao banco de dado

    # Criar as tabelas se não existire

    # Lista de tickers para buscar os dados
    tickers = ('BBDC3', 'VALE3', 'KLBN4', 'ITSA4', 'BRBI11', 'BLAU3', 'CLSC3','TRPL4','BBAS3','CMIG4','FESA4','SLCE3')

    # Inserir dados das ações e indicadores
    inserir_indicadores(tickers)


if __name__ == "__main__":
    main()