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
            SELECT A.*, I.* 
            FROM 
                ACOES AS A
            INNER JOIN 
                INDICADORES AS I 
            ON 
                A.ID = I.ACAO_ID
        """
        resultados = consultaBanco.executaSql(sql)

        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        indicadores_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return indicadores_json

class acao:

    def getCamposAcao(pTicker):
        sql = """
            SELECT 
                A.* 
            FROM 
                ACOES AS A
            WHERE 
                A.CODIGO = %s
        """
        resultados = consultaBanco.executaSql(sql, (pTicker,))

        if not resultados:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})

        acao_json = json.dumps(resultados, default=str, indent=4, ensure_ascii=False)
        return acao_json
   
