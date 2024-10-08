from app.models.conexaoBanco import conectarBanco
import json

class indicadores:

    def listAcoesDisponiveis():
        
        conexao = conectarBanco.retornaConexaoBanco()

        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT 
                A.CODIGO 
            FROM 
                ACOES AS A
        """)               
        
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
        cursor.execute(sql, (pTicker,))
        
        colunas = [desc[0] for desc in cursor.description]
        resultados = cursor.fetchall()
        
        acao = [dict(zip(colunas, row)) for row in resultados]
        
        cursor.close()
        conexao.close()
        
        acao_json = json.dumps(acao, default=str, indent=4, ensure_ascii=False)
        
        return acao_json
   
