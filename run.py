import logging
from app import create_app  # Supondo que você tenha uma função create_app em __init__.py

# Inicialize a aplicação Flask
app = create_app()

if __name__ == "__main__":
    # Configure o logging para o modo de depuração
    logging.basicConfig(level=logging.DEBUG)
    # Execute a aplicação Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
