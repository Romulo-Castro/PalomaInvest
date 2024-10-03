from app.models.conexaoBanco import conectarBanco as con
import json

def listAllIndicadores():
    try:
        conexao = con.retornaConexaoBanco()
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
    
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")

listAllIndicadores()
