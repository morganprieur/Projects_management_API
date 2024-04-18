
# Projects Management API 

## Description 
API de support B2B développée avec Django RestFramework. Elle permet de gérer des utilisateurs, des projets, des tickets et des commentaires de tickets. L'authentification par JWT est obligatoire, les utilisateur peuvent choisir d'autoriser le partage de leurs données et d'être contactés, créer des projets, tickets et commentaires, mais ne peuvent modifier ou supprimer que les leurs. 
Développement selon les princpes "green code" de l'INR, et respect de certaines règles du RGPD (consentement, accès, rectification, modification des données et choix de partage). 

## Installation 

1. **Variables d'environnement du projet** 

Vérifier que le fichier .env est présent et contient les variables utiles pour le projet (la clé dde sécurité de Django, les informations de connexion à la BDD) 


2. **Environnement virtuel (Pipenv)** 
(Doc)[https://pypi.org/project/pipenv/] 

21. Initialiser l'env. virtuel : `pipenv install` 
    Installation des dépendances 
22. Activer l'env. virtuel : `pipenv shell` 
    --> le nom du terminal devient "pipenv" 
23. Pour arrêter l'env. virtuel : `exit` 


3. **Lancer le serveur Django** 

31. `pipenv run python <chemin/vers>/manage.py runserver` 
32. Pour arrêter le serveur : `Ctrl+c` 


4. Visiter l'adresse `http://127.0.0.1:8000/` dans un navigateur pour vérifier le projet fonctionne. 
Cette adresse est la racine du projet d'API, dans un navigateur ou via Postman. 


## Tests 

Seulement les tests pour vérifier la création d'enregistrements par les signaux. 

*  Emplacement du fichier de test :    
`api/users/tests.py`    

*  Lancer les tests :     
`pipenv install` 
`pipenv shell` 
`cd api/` 
`python manage.py test users.tests -v 3` 
Régler le degré de détails avec `-v` : `3` = le maximum    




