import psycopg2

class conectarBanco:
    
    def retornaConexaoBanco():
        try:
            connection = psycopg2.connect(
                host="127.0.0.1",
                database="paloma_teste",
                user="postgres",
                #password="123"
                password="postgres"                
            )   
            return connection
        
        except Exception as e:
            raise Exception(f"Erro ao conectar com o banco de dados: {e}")
        
class consultaBanco:
        
    def executaSql(sql, params=None):
        conexao = conectarBanco.retornaConexaoBanco()
        cursor = conexao.cursor()

        try:
            if params:
                cursor.execute(sql, params)  # Executa com parâmetros (se fornecido)
            else:
                cursor.execute(sql)  # Executa sem parâmetros
                
            resultados = cursor.fetchall()

            # Nomes das colunas
            colunas = [desc[0] for desc in cursor.description]
            resultado_final = [dict(zip(colunas, row)) for row in resultados]
            
            return resultado_final

        except Exception as e:
            raise Exception(f"Erro ao executar SQL: {e}")
        
        finally:
            cursor.close()
            conexao.close()

