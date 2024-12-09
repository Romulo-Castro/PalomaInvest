from app.models.conexaoBanco import consultaBanco
from app.utils.jsonUtils import to_json, ErrorMessages as em
import json
import yfinance as yf

import yfinance as yf
import json
from datetime import datetime

class IndicadoresHistoricos:
    def __init__(self, ticker, indicador):
        self.ticker = ticker + ".SA"  # Adicionando o sufixo ".SA" para ações BR
        self.indicador = indicador

    def getIndicadoresHistoricos(self):
        if self.indicador == 'cot':
            return self.getCotacaoHistorica()
        elif self.indicador == 'pvp':
            return self.getPvpHistorico()      
        else:
            return to_json(None, em.INVALID_TICKER.value)

    def getCotacaoHistorica(self):
        try:
            acao = yf.Ticker(self.ticker)
            historico_precos = acao.history(period="5y")  
            cotacao_historica = historico_precos['Close']

            cotacao_historica_lista = [
                {"data": date.strftime('%Y-%m-%d'), "preco_fechamento": valor}
                for date, valor in cotacao_historica.items()
            ]
            return cotacao_historica_lista
        except Exception as e:
            return to_json(None, f"{em.UNKNOWN_ERROR.value}: {e}")

    def getPvpHistorico(self):
        try:
            acao = yf.Ticker(self.ticker)
            cotacao_historica = acao.history(period="5y", interval='3mo') 

            valor_patrimonial_total = acao.info.get('bookValue', None)
            if valor_patrimonial_total:
                pvp_valores = [
                    item.Close / valor_patrimonial_total
                    for item in cotacao_historica.itertuples()
                ]
                media_pvp = sum(pvp_valores) / len(pvp_valores)

                return to_json({"media_pvp": media_pvp})
            else:
                return to_json(None, em.NO_DATA_FOUND.value)
        except Exception as e:
            return to_json(None, f"{em.UNKNOWN_ERROR.value}: {e}")
        
class Indicadores:
    @staticmethod
    def listAcoesDisponiveis():
        try:
            sql = """
                SELECT 
                    A.CODIGO 
                FROM 
                    ACOES AS A
            """
            resultados = consultaBanco.executaSql(sql)
            return resultados
        except Exception as e:
            return to_json(None, f"{em.DATABASE_ERROR.value}: {e}")

    @staticmethod
    def listAllIndicadores():
        try:
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
            return resultados
        except Exception as e:
            return to_json(None, f"{em.DATABASE_ERROR.value}: {e}")


class Acao:
    @staticmethod
    def getCamposAcao(pTicker):
        try:
            sql = """
                SELECT 
                    A.* 
                FROM 
                    ACOES AS A
                WHERE 
                    A.CODIGO = %s
            """
            resultados = consultaBanco.executaSql(sql, (pTicker,))
            return resultados
        except Exception as e:
            return to_json(None, f"{em.DATABASE_ERROR.value}: {e}")

    @staticmethod
    def getAcoesDetalhes(pTicker):
        try:
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
                ORDER BY I.DATA_ULTIMA_COTACAO DESC
                LIMIT 1               
            """
            resultados = consultaBanco.executaSql(sql, (pTicker,))
            return resultados
        except Exception as e:
            return to_json(None, f"{em.DATABASE_ERROR.value}: {e}")


# Funções externas
def obterAcoesDisponiveis():
    return Indicadores.listAcoesDisponiveis()

def obterTodosIndicadores():
    return Indicadores.listAllIndicadores()

def obterIndicadorHistorico(pTicker, pIndicador):
    indicadores = IndicadoresHistoricos(pTicker, pIndicador)
    return indicadores.getIndicadoresHistoricos()

def obterCamposAcao(pTicker):
    return Acao.getCamposAcao(pTicker)

def obterAcoesDetalhes(pTicker):
    return Acao.getAcoesDetalhes(pTicker)
