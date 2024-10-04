from app.models.conexaoBanco import conectarBanco
import json

class indicadores:

    def listAcoesDisponiveis():
        try:
            conexao = conectarBanco.retornaConexaoBanco()
            cursor = conexao.cursor()
            
            cursor.execute("""
                SELECT 
                    A.CODIGO 
                FROM 
                    ACOES AS A
            """)  

        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")                      
        
        colunas = [desc[0] for desc in cursor.description]
        
        resultados = cursor.fetchall()
        acoes = [dict(zip(colunas, row)) for row in resultados]
            
        cursor.close()
        conexao.close()
        
        # Converte para JSON 
        acoes_json = json.dumps(acoes, default=str, indent=4, ensure_ascii=False)
        
        print(acoes_json)
        
        return acoes_json        

    def listAllIndicadores():
        try:
            conexao = conectarBanco.retornaConexaoBanco()
            cursor = conexao.cursor()
            
            cursor.execute("""
                SELECT A.*, I.* 
                FROM 
                    ACOES AS A
                INNER JOIN 
                    INDICADORES AS I 
                ON 
                    A.ID = I.ACAO_ID
            """)
        
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")

        # nomes das colunas
        colunas = [desc[0] for desc in cursor.description]
        
        resultados = cursor.fetchall()
        indicadores = [dict(zip(colunas, row)) for row in resultados]
            
        cursor.close()
        conexao.close()
        
        # Converte para JSON 
        indicadores_json = json.dumps(indicadores, default=str, indent=4, ensure_ascii=False)
        
        print(indicadores_json)
        
        return indicadores_json            