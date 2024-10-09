import psycopg2

# Função para conectar ao banco de dados PostgreSQL
def conectar():
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="paloma_teste",
            user="postgres",
            password="aluno"
        )   
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

# Função para criar as tabelas, caso elas não existam
def criar_tabelas(conn):
    try:
        cur = conn.cursor()

        # Criação da tabela acoes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.acoes (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(10) NOT NULL,
                nome_empresa VARCHAR(255) NOT NULL,
                setor VARCHAR(255),
                tipo VARCHAR(10)
            );
        """)

        # Criação da tabela indicadores
        cur.execute(
        """
            CREATE TABLE IF NOT EXISTS public.indicadores (
            id SERIAL PRIMARY KEY,
            acao_id INT REFERENCES public.acoes(id),
            credito NUMERIC(20,2),
            depositos NUMERIC(20,2),
            result_inter_financ_12m NUMERIC(20,2),
            receita_servicos_12m NUMERIC(20,2),
            result_inter_financ_3m NUMERIC(20,2),
            receita_servicos_3m NUMERIC(20,2),
            disponibilidades NUMERIC(20,2),
            ativo_circulante NUMERIC(20,2),
            divida_bruta NUMERIC(20,2),
            divida_liquida NUMERIC(20,2),
            receita_liquida_12m NUMERIC(20,2),
            ebit_12m NUMERIC(20,2),
            receita_liquida_3m NUMERIC(20,2),
            ebit_3m NUMERIC(20,2),
            cotacao NUMERIC(20,2),
            min_52_sem NUMERIC(20,2),
            max_52_sem NUMERIC(20,2),
            vol_med_2m NUMERIC(20,2),
            valor_de_mercado NUMERIC(20,2),
            valor_da_firma NUMERIC(20,2),
            ult_balanco_processado DATE,
            nro_acoes NUMERIC(20,2),
            pl NUMERIC(20,2),
            pvp NUMERIC(20,2),
            pebit NUMERIC(20,2),
            psr NUMERIC(20,2),
            pativos NUMERIC(20,2),
            pcap_giro NUMERIC(20,2),
            pativ_circ_liq NUMERIC(20,2),
            div_yield NUMERIC(20,2),
            ev_ebitda NUMERIC(20,2),
            ev_ebit NUMERIC(20,2),
            cres_rec_5a NUMERIC(20,2),
            lpa NUMERIC(20,2),
            vpa NUMERIC(20,2),
            margem_bruta NUMERIC(20,2),
            margem_ebit NUMERIC(20,2),
            margem_liquida NUMERIC(20,2),
            ebit_ativo NUMERIC(20,2),
            roic NUMERIC(20,2),
            roe NUMERIC(20,2),
            liquidez_corrente NUMERIC(20,2),
            div_bruta_patrim NUMERIC(20,2),
            giro_ativos NUMERIC(20,2),
            ativo NUMERIC(20,2),
            lucro_liquido_12m NUMERIC(20,2),
            lucro_liquido_3m NUMERIC(20,2),
            patrim_liq NUMERIC(20,2),
            data_ultima_cotacao DATE,    
            data_atualizacao DATE
            );
        """)

        # Commit para salvar as alterações
        conn.commit()
        cur.close()
        print("Tabelas criadas ou já existem.")
    
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        conn.rollback()

# Função principal
def main():
    # Conectar ao banco de dados
    conn = conectar()
    
    if conn is not None:
        # Criar as tabelas se não existirem
        criar_tabelas(conn)

        # Fechar a conexão
        conn.close()

if __name__ == "__main__":
    main()
