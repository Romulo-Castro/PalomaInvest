from app.models.conexaoBanco import consultaBanco
import json

class indicadores:

    def listAcoesDisponiveis():
        sql = """
            SELECT 
                A.CODIGO 
            FROM 
                ACOES AS A
        """
        resultados = consultaBanco.executaSql(sql)

        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        # Converte para JSON
        acoes_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return acoes_json       

    def listAllIndicadores():
        sql = """
            SELECT DISTINCT ON (A.ID) A.*, I.*
            FROM 
                ACOES AS A
            INNER JOIN 
                INDICADORES AS I 
            ON 
                A.ID = I.ACAO_ID
            ORDER BY A.ID, I.DATA_ULTIMA_COTACAO DESC
        """
        resultados = consultaBanco.executaSql(sql)

        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        indicadores_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return indicadores_json

class acao:

    def getCamposAcao(pTicker):
        sql = """
            SELECT A.*, I.* 
            FROM 
                ACOES AS A
            INNER JOIN 
                INDICADORES AS I 
            ON 
                A.ID = I.ACAO_ID
            WHERE 
                A.CODIGO = %s
            ORDER BY I.DATA_ATUALIZACAO DESC
                LIMIT 1
        """
        resultados = consultaBanco.executaSql(sql, (pTicker,))

        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        acao_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return acao_json
    
    def getAcoesDetalhes(pTicker):
        sql = """
            SELECT A.*, I.* 
            FROM 
                ACOES AS A
            INNER JOIN 
                INDICADORES AS I 
            ON 
                A.ID = I.ACAO_ID
            WHERE 
                A.CODIGO = %s                
        """
        resultados = consultaBanco.executaSql(sql, (pTicker,))
        
        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        acaoDetalhes_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return acaoDetalhes_json     
    
def obterAcoesDisponiveis():
    return indicadores.listAcoesDisponiveis()

def obterTodosIndicadores():
    return indicadores.listAllIndicadores()

def obterCamposAcao(pTicker):
    return acao.getCamposAcao(pTicker)

def obterAcoesDetalhes(pTicker):
    return acao.getAcoesDetalhes(pTicker)
   