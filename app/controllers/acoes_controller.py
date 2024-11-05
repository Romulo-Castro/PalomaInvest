from app.models import model_acoes as mAcoes
from flask import request
import json

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
            return acao
        else:
            return json.dumps({"status": "error", "message": "Ticker não especificado."})
     
    def getAcaoDetalhes(self):
        pTicker = request.args.get('codigo')

        if pTicker:
            acaoDetalhes = mAcoes.obterAcoesDetalhes(pTicker.upper())
            return acaoDetalhes
        else:
            return json.dumps({"status": "error", "message": "Ticker não especificado."})      