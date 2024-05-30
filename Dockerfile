# Utiliser une image de base officielle de Python
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de configuration et le code de l'application dans le répertoire de travail
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY db_setup.py db_setup.py
COPY models models
COPY database.db database.db

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application va tourner
EXPOSE 5000

# Définir la commande par défaut pour exécuter l'application
CMD ["python", "app.py"]
