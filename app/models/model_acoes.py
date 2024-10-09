from app.models.conexaoBanco import conectarBanco
import json

class indicadores:

    def listAcoesDisponiveis():
        
        conexao = conectarBanco.retornaConexaoBanco()

        cursor = conexao.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    A.CODIGO 
                FROM 
                    ACOES AS A
            """)             
        except Exception as e:
            raise Exception(f"Tabela não existe no banco: {e}")
        
        resultados = cursor.fetchall()
        
        # se select vazio -> early return JSON vazio
        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})
            
        colunas = [desc[0] for desc in cursor.description]
        
        acoes = [dict(zip(colunas, row)) for row in resultados]
            
        cursor.close()
        conexao.close()
        
        # Converte para JSON 
        acoes_json = json.dumps(acoes, default=str, indent=4, ensure_ascii=False)
        
        print(acoes_json)
        
        return acoes_json        

    def listAllIndicadores():

        conexao = conectarBanco.retornaConexaoBanco()
        cursor = conexao.cursor()
        
        try: 
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
            raise Exception(f"Tabela não existe no banco: {e}")        

        resultados = cursor.fetchall()
        
        # se select vazio -> early return JSON vazio
        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})
            
        # nomes das colunas
        colunas = [desc[0] for desc in cursor.description]
        
        indicadores = [dict(zip(colunas, row)) for row in resultados]
            
        cursor.close()
        conexao.close()
        
        # Converte para JSON 
        indicadores_json = json.dumps(indicadores, default=str, indent=4, ensure_ascii=False)
        
        print(indicadores_json)
        
        return indicadores_json   

class acao:

    def getCamposAcao(pTicker):
        conexao = conectarBanco.retornaConexaoBanco()
        cursor = conexao.cursor()

        sql = """
            SELECT 
                A.* 
            FROM 
                ACOES AS A
            WHERE 
                A.CODIGO = %s 
        """                  
        
        try:
            cursor.execute(sql, (pTicker,))
        except Exception as e:
            raise Exception(f"Tabela não existe no banco: {e}")          
        
        resultados = cursor.fetchall()
        
        # se select vazio -> early return JSON vazio
        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})
        
        colunas = [desc[0] for desc in cursor.description]
        
        acao = [dict(zip(colunas, row)) for row in resultados]
        
        cursor.close()
        conexao.close()
        
        acao_json = json.dumps(acao, default=str, indent=4, ensure_ascii=False)
        
        return acao_json
   
