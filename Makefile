VENV_DIR = venv

# Comando para criar e ativar o ambiente virtual
setup:
	if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Criando ambiente virtual..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	# Usando bash -c para garantir que a ativação aconteça no mesmo shell
	bash -c "source $(VENV_DIR)/bin/activate && pip install -r requirements.txt"
