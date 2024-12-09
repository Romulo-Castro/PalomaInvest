from app.models.model_acoes import obterAcoesDetalhes
from app.utils.jsonUtils import to_json, ErrorMessages as em
import google.generativeai as genai
import math

class AiService:

    def __init__(self, ticker):
        genai.configure(api_key="AIzaSyC1qCBg76qEnyTCkATqmNO8WuQJnr_eEwM")
        self.model = genai.GenerativeModel("gemini-1.5-flash")  
        self.ticker = ticker

    def getTextoPadrao(self):
        return """
            Analise detalhadamente a ação {ticker}.
            Utilize os seguintes dados financeiros para construir uma tese de investimento abrangente, destacando pontos fortes, fracos, oportunidades e ameaças relacionadas ao ativo:

            {dados}

            Objetivos da análise:

                Compare o P/L da empresa com a média do setor para avaliar se a ação está sobre ou subavaliada.
                Avalie a atratividade do Dividend Yield em relação à taxa básica de juros (como a Selic) ou outros investimentos de renda fixa.
                Explique se o ROE é satisfatório e o que ele indica sobre a eficiência da empresa em gerar lucro com seu patrimônio.
                Identifique desafios e oportunidades no setor de atuação da empresa e como isso pode impactar o desempenho futuro do ativo.
                Considere o preço atual e avalie se há uma margem de segurança adequada para a compra.

            Com base nesses pontos, responda às seguintes perguntas na tese:

                A ação está bem avaliada no preço atual?
                Qual é a principal vantagem competitiva da empresa em seu setor?
                O que pode ameaçar o desempenho futuro do ativo?
                O que torna essa ação uma oportunidade (ou não) para investidores?

            Nota: O texto gerado deve ser claro, objetivo e estruturado para que qualquer investidor iniciante ou educador possa compreender facilmente.                    
            
            Além disso, faça o cálculo do valor Intrínseco de Graham (Raiz Quadrada de ((PL * PVP) * LPA * VPA)) e plote no final da resposta.
        """

    def calculaValorIntrinseco(self, dadosUsuario, dadosTese):
        lpa = dadosTese['lpa']
        vpa = dadosTese['vpa']

        if dadosUsuario:
            constanteGraham = (dadosUsuario['pl'] * dadosUsuario['pvp'])
            vi = math.sqrt(constanteGraham * float(lpa) * float(vpa))  # Converte para float
            return vi

        constanteGraham = (dadosTese['pl'] * dadosTese['pvp'])
        vi = math.sqrt(constanteGraham * float(lpa) * float(vpa))  # Converte para float
        return vi


    def obterDadosFinanceiros(self):
        try:
            dados = obterAcoesDetalhes(self.ticker)  # Busca dados do banco
            print(dados)
            if not dados:
                raise ValueError(em.NO_DATA_FOUND.value)
            return dados
        
        except Exception as e:
            return to_json({"status": "error", "message": em.DATABASE_ERROR.value.format(e)})
        
    def filtrarIndicadoresTese(self):
        dados = self.obterDadosFinanceiros()

        if not isinstance(dados, list) or (isinstance(dados, dict) and "status" in dados and dados["status"] == "error"):
            print("Erro ao obter dados financeiros:", dados)
            return None

        campos_relevantes = [
            "codigo", "nome_empresa", "setor", "tipo",
            "cotacao", "pl", "pvp", "div_yield", "roe", 
            "lucro_liquido_12m", "cres_rec_5a", "patrim_liq",
            "valor_de_mercado", "ativo", "data_ultima_cotacao",
            "vpa", "lpa"
        ]

        # Assume que `dados` é uma lista de resultados (pegando o primeiro item)
        dados = dados[0] if isinstance(dados, list) and len(dados) > 0 else dados
        dados_filtrados = {campo: dados.get(campo) for campo in campos_relevantes}

        return dados_filtrados

        

class AI:
    def __init__(self, ticker):
        self.service = AiService(ticker)      
    
    def gerarTese(self, dadosUsuario):
        dadosTese = self.service.filtrarIndicadoresTese()

        dados_formatados = "\n".join(
            f"- {campo.replace('_', ' ').capitalize()}: {valor}"
            for campo, valor in dadosTese.items()
        )        

        # Formata o texto padrão
        texto_padrao = self.service.getTextoPadrao().format(
            ticker=self.service.ticker,
            dados=dados_formatados
        )   

        valorIntinseco = self.service.calculaValorIntrinseco(dadosUsuario, dadosTese)

        # Gera texto com o modelo Gemini
        try:
            resposta = self.service.model.generate_content(texto_padrao)
            return to_json({"vi": valorIntinseco,"tese": resposta.text, "dados": dadosTese, "prompt": texto_padrao})
        except Exception as e:
            return to_json({"status": "error", "message": em.AI_GENERATION_ERROR.value.format(e)})

def getTese(pTicker, pDados):
    Ai = AI(pTicker)
    return Ai.gerarTese(pDados)