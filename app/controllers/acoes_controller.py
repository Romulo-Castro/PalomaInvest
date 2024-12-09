from app.models import model_acoes as mAcoes
from flask import request
from app.utils.jsonUtils import to_json, ErrorMessages as em

class AcoesController:
   
    def home(self):
        listaCodigoAcoesDisponiveis = mAcoes.obterAcoesDisponiveis()        
        return listaCodigoAcoesDisponiveis
    
    def listAllAcoesIndicadores(self):
        listaTodosIndicadores = mAcoes.obterTodosIndicadores()
        return listaTodosIndicadores
    
    def getAcao(self):
        pTicker = request.args.get('codigo')
        
        if pTicker:
            acao = mAcoes.obterCamposAcao(pTicker.upper())
            return to_json(acao, em.NO_DATA_FOUND.value)
        else:
            return to_json(None, em.INVALID_TICKER.value)
     
    def getAcaoDetalhes(self):
        pTicker = request.args.get('codigo')

        if pTicker:
            acaoDetalhes = mAcoes.obterAcoesDetalhes(pTicker.upper())
            return to_json(acaoDetalhes, em.NO_DATA_FOUND.value)
        else:
            return to_json(None, em.INVALID_TICKER.value)      
        
    def getCotacaoHistorica(self):
        pTicker = request.args.get('codigo')

        if pTicker:
            acaoDetalhes = mAcoes.obterCotacaoHistorica(pTicker.upper())
            return to_json(acaoDetalhes, em.NO_DATA_FOUND.value)
        else:
            return to_json(None, em.INVALID_TICKER.value)      

    def getIndicadorHistorico(self):
        pTicker = request.args.get('codigo')
        pIndicador = request.args.get('ind')

        if pTicker and pIndicador:
            acaoDetalhes = mAcoes.obterIndicadorHistorico(pTicker.upper(), pIndicador.lower())
            return to_json(acaoDetalhes, em.NO_DATA_FOUND.value)
        elif not pTicker:
            return to_json(None, em.INVALID_TICKER.value)
        elif not pIndicador:
            return to_json(None, "Indicador não especificado.")
