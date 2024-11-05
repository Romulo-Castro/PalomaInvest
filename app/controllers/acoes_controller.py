from app.models import model_acoes as mAcoes

class AcoesController:
   
    def home(self):
        listaCodigoAcoesDisponiveis = mAcoes.obterAcoesDisponiveis()        
        return listaCodigoAcoesDisponiveis

    
    def listAllAcoesIndicadores(self):
        listaTodosIndicadores = mAcoes.obterTodosIndicadores()
        return listaTodosIndicadores
    
    def getAcao(self, pTicker):
        acao = mAcoes.obterCamposAcao(pTicker.upper())
        return acao
     
    def getAcaoDetalhes(self, pTicker):
        acaoDetalhes = mAcoes.obterAcoesDetalhes(pTicker.upper())
        return acaoDetalhes        