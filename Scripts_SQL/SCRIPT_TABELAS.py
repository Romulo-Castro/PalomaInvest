import fundamentus
import psycopg2
from datetime import datetime

# Função para conectar ao banco de dados PostgreSQL
def conectar():
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="paloma",
            user="postgres",
            password="paloma"
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
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.indicadores (
                id SERIAL PRIMARY KEY,
                acao_id INT REFERENCES public.acoes(id),
                cotacao NUMERIC(10,2),
                pl NUMERIC(10,2),
                pvp NUMERIC(10,2),
                dy NUMERIC(5,2),
                lpa NUMERIC(10,2),
                vpa NUMERIC(10,2),
                margem_ebit NUMERIC(5,2),
                margem_liquida NUMERIC(5,2),
                roe NUMERIC(5,2),
                roic NUMERIC(5,2),
                liq_corrente NUMERIC(10,2),
                div_bruta_patr NUMERIC(5,2),
                cres_rec_5a NUMERIC(5,2),
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

def printarQry(ticker, dados):
    qry = f"""
        ticker {ticker} 
        , cotacao {dados[1]}
        , pl {dados[2]}
        , pvp {dados[3]}
        , dy {dados[4]}
        , lpa {dados[5]}
        , vpa {dados[6]}
        , margem_ebit {dados[7]}
        , margem_liquida {dados[8]}
        , roe {dados[9]}
        , roic {dados[10]}
        , liq_corrente {dados[11]}
        , div_bruta_patr {dados[12]}
        , cres_rec_5a {dados[13]}
        , data_atualizacao {dados[14]}
    """   
    print("Query:")
    print(qry)

def inserir_acoes(conn, tickers):
    try:
        cur = conn.cursor()

        # Comando SQL para inserção dos dados
        insert_query = """
            INSERT INTO acoes (codigo, nome_empresa, setor, tipo)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """

        select_query = "SELECT id FROM acoes WHERE codigo = %s"

        # Iterar sobre os tickers fornecidos
        for valor in tickers:
            df = fundamentus.get_papel(valor)
            ticker = valor
            nome_empresa = df['Empresa'].iloc[0]
            setor = df['Setor'].iloc[0]
            tipo = df['Tipo'].str.split().str[0].iloc[0]

            # Verificar se o ticker já existe
            cur.execute(select_query, (ticker,))
            acao_id = cur.fetchone()

            if acao_id is None:
                # Inserir o novo ticker se não existir
                cur.execute(insert_query, (ticker, nome_empresa, setor, tipo))
                acao_id = cur.fetchone()[0]
                print(f"Ação inserida com ID: {acao_id}")
            else:
                acao_id = acao_id[0]
                print(f"Ação já existe com ID: {acao_id}")

        # Commit para salvar as alterações no banco
        conn.commit()
        cur.close()
        return acao_id  # Retorna o ID da última ação inserida
    
    except Exception as e:
        print(f"Erro ao inserir dados de ações: {e}")
        conn.rollback()


# Função para inserir os dados de indicadores no banco de dados
def inserir_indicadores(conn, tickers):
    try:
        cur = conn.cursor()
        
        # Obter os dados de fundamentus
        df = fundamentus.get_resultado()
        for index, row in df.iterrows():
            ticker = index
            if ticker in tickers:
                cotacao = row['cotacao']
                pl = row['pl']
                pvp = row['pvp']
                lpa = cotacao / pl if pl != 0 else 0
                vpa = cotacao / pvp if pvp != 0 else 0
                dy = row['dy']
                margem_ebit = row['mrgebit']
                margem_liquida = row['mrgliq']
                roe = row['roe']
                roic = row['roic']
                liq_corrente = row['liqc']
                div_bruta_patr = row['divbpatr']
                cres_rec_5a = row['c5y']
                data_atualizacao = datetime.now().date()
                
                # Obter o ID da ação correspondente
                cur.execute("SELECT id FROM acoes WHERE codigo = %s", (ticker,))
                acao_id = cur.fetchone()[0]

                indicadores = (
                    acao_id
                    , cotacao
                    , pl
                    , pvp
                    , dy
                    , lpa
                    , vpa
                    , margem_ebit
                    , margem_liquida
                    , roe
                    , roic
                    , liq_corrente
                    , div_bruta_patr
                    , cres_rec_5a
                    , data_atualizacao 
                )

                printarQry(ticker, indicadores)
                
                # Comando SQL para inserção dos dados de indicadores
                query = """
                    INSERT INTO indicadores 
                    (
                        acao_id, cotacao, pl, pvp, dy, lpa, vpa,
                        margem_ebit, margem_liquida, roe, roic,
                        liq_corrente, div_bruta_patr, cres_rec_5a, data_atualizacao
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Inserir os dados de indicadores no banco de dados
                cur.execute(query, indicadores)

        # Commit para salvar as alterações no banco
        conn.commit()
        cur.close()
        print("Dados dos indicadores inseridos com sucesso!")
    
    except Exception as e:
        print(f"Erro ao inserir dados de indicadores: {e}")
        conn.rollback()

# Função principal
def main():
    # Conectar ao banco de dados
    conn = conectar()
    
    if conn is not None:
        # Criar as tabelas se não existirem
        criar_tabelas(conn)

        # Lista de tickers para buscar os dados
        tickers = ('ITUB4', 'BBDC3', 'VALE3', 'BBDC4', 'CMIG4', 'WEGE3')

        # Inserir dados das ações no banco
        inserir_acoes(conn, tickers)

        # Inserir dados dos indicadores no banco
        inserir_indicadores(conn, tickers)

        # Fechar a conexão com o banco
        conn.close()

if __name__ == "__main__":
    main()
