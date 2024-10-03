from app.models import model_info_acoes as mInfoAcoes

class AcoesController:
    def listAllAcoesIndicadores(self):
        return mInfoAcoes.listAllIndicadores()