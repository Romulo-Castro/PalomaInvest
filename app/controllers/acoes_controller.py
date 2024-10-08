from app.models import model_acoes as mAcoes

class AcoesController:
   
    def home(self):
        model = mAcoes.indicadores

        listaCodigoAcoesDisponiveis = model.listAcoesDisponiveis()
        
        return listaCodigoAcoesDisponiveis

    
    def listAllAcoesIndicadores(self):
        model = mAcoes.indicadores

        listaTodosIndicadores = model.listAllIndicadores()

        return listaTodosIndicadores
    
    def getAcao(self, pTicker):
        model = mAcoes.acao

        acao = model.getCamposAcao(pTicker)

        return acao
     