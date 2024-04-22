
# Projects Management API 

## Description 

Django RestFramework B2B support API. 
It allows to manage users, projects, issues and issues' comments. Authentication is ensured by JWT. The users chose to share or not their data, and to be contacted or not, and they are allowed to manage their choices even they want it. 
The logged in users can create projects, issues, and issues' comments, and manage their own objects. 
The API respects "green code" of "INR" and some rules of the GDPR about the users' data. 

The documentation has been generated with DRF Spectacular. 

The (PostgreSQL) DB and the API are running into different Docker containers. 


## Installation 

1. **Variables d'environnement du projet** 

Vérifier que le fichier .env est présent et contient les variables utiles pour le projet (la clé dde sécurité de Django, les informations de connexion à la BDD) 


2. **Environnement virtuel (Pipenv)** 
[Doc](https://pypi.org/project/pipenv/) 

* Initialiser l'env. virtuel : `pipenv install` 
    Installation des dépendances
* Activer l'env. virtuel : `pipenv shell` 
    --> le nom du terminal devient "pipenv"    
* Pour arrêter l'env. virtuel : `exit` 


3. **Lancer le serveur Django** 

* `pipenv run python <chemin/vers>/manage.py runserver` 
* Pour arrêter le serveur : `Ctrl+c` 


4. Visiter l'adresse `http://127.0.0.1:8000/` dans un navigateur pour vérifier le projet fonctionne. 
Cette adresse est la racine du projet d'API, dans un navigateur ou via Postman. 


## Tests 

Seulement les tests pour vérifier la création d'enregistrements par les signaux. 

*  Emplacement du fichier de test :    
`api/users/tests.py`    

*  Lancer les tests :     
`cd api/`     
`python manage.py test users.tests -v 3`     
Régler le degré de détails avec `-v` : `3` = le maximum    




