from mvc_flask import Router

Router.get('/', 'acoes#home')
Router.get('/detalhes', 'acoes#listAllAcoesIndicadores')

"""
Router.all("messages")
Router.all("callbacks", only="index show")

api = Router.namespace("/api/v1")

api.get("/health", "health#index")

posts = api.namespace("/posts")
posts.all("posts", only="index")
"""