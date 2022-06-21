# P9

Télécharger/cloner le dépôt *P9 (branche master)*

Créer un environnement virtuel dans le répertoire P9 créé localement : `python -m venv env`

activer l'environnement virtuel : `source env/bin/activate` (Linux) 
                                ou `env\\Scripts\\activate.bat` (terminal Windows)
                                ou `env\\Scripts\\activate.PS1` (Windows PowerShell)

installer les modules requis à partir du fichier requirements.txt : `pip install -r requirements`

Se placer dans le dossier *litreview/*

Y copier le fichier *.env* contenant la SECRET_KEY nécessaire au projet

Lancer le serveur avec la commande `python manage.py runserver`

Ouvrir le navigateur internet à l'adresse http://127.0.0.1:8000/login/


# Remarque :

Hors démonstration, ce projet ne comporte aucune donnée.

L'utilisateur/développeur qui installe les fichiers du présent projet doit donc exécuter les commandes suivantes pour initialiser la base de données :

`python manage.py makemigrations`, puis `python manage.py migrate`.
