from app.models.model_acoes import obterAcoesDetalhes
import json
import yfinance as yf
import pandas as pd
import google.generativeai as genai

def _to_json(data):
    if not data:
        return json.dumps({"status": "error", "message": "Nenhum dado encontrado."})
    else:
        return json.dumps(data, default=str, indent=4, ensure_ascii=False)

class AI:

    def __init__(self, ticker):
        genai.configure(api_key="AIzaSyC1qCBg76qEnyTCkATqmNO8WuQJnr_eEwM")
        self.model = genai.GenerativeModel("gemini-1.5-flash")  
        self.ticker = ticker

    def getTextoPadrao(self):
        return """
            Analise a ação {ticker}.

            Considere os seguintes dados financeiros e forneça uma tese de investimento detalhada, 
            abordando os pontos fortes, fracos e possíveis oportunidades ou ameaças relacionadas ao ativo. 
            Baseie-se nos seguintes aspectos:

            {dados}

            Contexto e objetivos:

            Compare o P/L com a média do setor para identificar se a ação está sobre ou subavaliada.
            Avalie a atratividade do Dividend Yield em relação à taxa básica de juros (ex.: Selic) ou outros investimentos de renda fixa.
            Explique se o ROE é satisfatório e o que isso sugere sobre a eficiência da empresa em gerar lucro com seu patrimônio.
            Identifique os desafios e oportunidades no setor de atuação da empresa e como isso pode impactar o desempenho futuro da ação.
            Considere o preço atual e avalie se há margem de segurança para compra.
            Com base nesses pontos, gere uma tese que responda:

            A ação está bem avaliada no preço atual?
            Qual a principal vantagem competitiva da empresa?
            O que pode ameaçar o desempenho futuro do ativo?
            O que faz da ação uma oportunidade (ou não) para investidores?
        """

    def obterDadosFinanceiros(self):
        try:
            dados = obterAcoesDetalhes(self.ticker)  # Busca dados do banco
#            if not dados or isinstance(dados, str):  # Verifica se não há resultados
 #               raise ValueError("Nenhum dado encontrado para o ticker fornecido.")

            return dados
        
        except Exception as e:
            return {"status": "error", "message": f"Erro ao obter dados do ticker {self.ticker}: {e}"}


    def gerarTese(self):
        # Recupera dados do ticker
        dados = self.obterDadosFinanceiros()
        if "status" in dados and dados["status"] == "error":
            return _to_json(dados)

        # Formata o texto padrão
        texto_padrao = self.getTextoPadrao().format(
            ticker=self.ticker,
            dados=dados
        )

        # Gera texto com o modelo Gemini
        try:
            resposta = self.model.generate_content(texto_padrao)
            return _to_json({"tese": resposta.text, "dados": dados, "prompt": texto_padrao})
        except Exception as e:
            return _to_json({"status": "error", "message": f"Erro ao gerar tese: {e}"})

def getTese(pTicker):
    Ai = AI(pTicker)
    return Ai.gerarTese()