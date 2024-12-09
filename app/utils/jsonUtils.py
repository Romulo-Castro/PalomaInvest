import json
from enum import Enum

class ErrorMessages(Enum):
    NO_DATA_FOUND = "Nenhum dado encontrado."
    INVALID_TICKER = "Ticker fornecido é inválido."
    DATABASE_ERROR = "Erro ao acessar o banco de dados."
    AI_GENERATION_ERROR = "Erro ao gerar a tese com IA."
    UNKNOWN_ERROR = "Erro desconhecido. Por favor, tente novamente mais tarde."

def to_json(data, error_message=None):
    if not data:
        return {"status": "error", "message": error_message or ErrorMessages.NO_DATA_FOUND.value}
    return data

