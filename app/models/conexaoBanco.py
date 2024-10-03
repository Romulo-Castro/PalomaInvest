import psycopg2

class conectarBanco:
    def retornaConexaoBanco():
        try:
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="paloma_teste",
                user="postgres",
                password="aluno"
            )   
            return conn
        
        except Exception as e:
            return e