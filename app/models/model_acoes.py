from app.models.conexaoBanco import consultaBanco
import json
import yfinance as yf
import pandas as pd

def _to_json(data):
    if not data:
            return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})
    else: return json.dumps(data, default=str, indent=4, ensure_ascii=False)

class indicadoresHistoricos:

    def __init__(self, ticker, indicador):
        self.ticker = ticker + ".SA"  # Adicionando o sufixo ".SA" para ações BR
        self.indicador = indicador

    def getIndicadoresHistoricos(self):
        if self.indicador == 'cot':
            return self.getCotacaoHistorica()
        elif self.indicador == 'pvp':
            return self.getPvpaHistorico()
        else:
            return {"erro": "Indicador não encontrado"}

    def getCotacaoHistorica(self):
        acao = yf.Ticker(self.ticker)
        historico_precos = acao.history(period="1y")  # Cotação Histórica de 1 ano
        cotacao_historica = historico_precos['Close']

        # Converter a série para uma lista de dicionários com a data como string
        cotacao_historica_lista = [{"data": date.strftime('%Y-%m-%d'), "preco_fechamento": valor} 
                                   for date, valor in cotacao_historica.items()]
        
        # Retorna a lista como JSON
        return _to_json(cotacao_historica_lista)

    def getPvpaHistorico(self):
        acao = yf.Ticker(self.ticker)
        cotacao_historica_json = self.getCotacaoHistorica()
        cotacao_historica = json.loads(cotacao_historica_json)  # Converte para lista de dicionários

        valor_patrimonial_por_acao = acao.info.get('bookValue')  # Valor patrimonial por ação

        if valor_patrimonial_por_acao:
            pvpa_historico = [{
                "data": item['data'],
                "pvpa": item['preco_fechamento'] / valor_patrimonial_por_acao
            } for item in cotacao_historica]

            return _to_json(pvpa_historico)
        else:
            return {"erro": "Valor patrimonial por ação não disponível"}


class indicadores:

    def listAcoesDisponiveis():
        sql = """
            SELECT 
                A.CODIGO 
            FROM 
                ACOES AS A
        """
        resultados = consultaBanco.executaSql(sql)

        # Converte para JSON
        return _to_json(resultados)

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

        return _to_json(resultados)
    

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

        return _to_json(resultados)
    
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
            ORDER BY I.DATA_ATUALIZACAO DESC
                LIMIT 1               
        """
        resultados = consultaBanco.executaSql(sql, (pTicker,))
        
        return _to_json(resultados)    
    
def obterAcoesDisponiveis():
    return indicadores.listAcoesDisponiveis()

def obterTodosIndicadores():
    return indicadores.listAllIndicadores()

def obterIndicadorHistorico(pTicker, pIndicador):
    indicadores = indicadoresHistoricos(pTicker, pIndicador) 
    return indicadores.getIndicadoresHistoricos()

def obterCamposAcao(pTicker):
    return acao.getCamposAcao(pTicker)

def obterAcoesDetalhes(pTicker):
    return acao.getAcoesDetalhes(pTicker)
   