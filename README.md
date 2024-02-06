
# Softdesk Support 

## Description 
API de support B2B développée avec Django RestFramework. Elle permet de gérer des utilisateurs, des projets, des tickets et des commentaires de tickets. L'authentification par JWT est obligatoire, les utilisateur peuvent choisir d'autoriser le partage de leurs données et être contactés, créer des projets, tickets et commentaires, mais ne peuvent modifier ou supprimer que les leurs. 
Développement selon les princpes "green code" de l'INR, et respect de certaines mesures du RGPD. 

## Installation 

1. **Environnement virtuel (Pipenv)** 
11. Initialiser l'env. virtuel : `pipenv install` 
12. Activer l'env. virtuel : `pipenv shell` (le nom du terminal devient "pipenv") 
13. Pour arrêter l'env. virtuel : `exit` 

2. **Installer Django et DRF** 
`pip install django psycopg2 djangorestframework` 
psycopg2 est indispensable avec PostgreSQL 

3. **Requirements.txt** 
Mettre à jour les requirements :`pip freeze > softdesk/requirements.txt` 

4. **Etapes BDD Django** 
4. Changer les données dans DATABASES du fichier settings.py, remplacer les données Sqlite3 par celles-ci :    
```python 
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('POSTGRES_NAME'),   # nom de la bdd 
    'USER': os.environ.get('POSTGRES_USER'),
    'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'HOST': '<softdesk_db>',   # nom du service 
    'PORT': 5432, 
``` 

5. **Utilisation de Docker** 
51. Builder le container : 
511. Dans compose.yaml, commenter la ligne "command..." 
512. Lancer la commande :    
`[sudo]* docker compose run <web>* django-admin startproject <nom_projet>* .` 
pour installer le projet Django. 
* 
sudo : selon votre configuration 
web : le nom du dossier contenant le Dockerfile 
nom_projet : le nom du projet à créer 
. : le dossier courant 

6. **Etape Application de Django** 
61. Installer une application Django :    
`cd <projet>` 
`python manage.py startapp <nom_de_la_application>` 
62. Ajouter l'application dans le fichier settings.py['INSTALLED_APPS'] 

7. **Lancer le container Docker** 
71. Ajouter la ligne :    
`command: bash -c "pwd && python manage.py runserver 0.0.0.0:${API_PORT}"` 
au fichier compose.yaml 
72. Rebuilder et lancer le container et le serveur django :    
`docker compose up --build --remove-orphans` 


8. **Vérifer que tout fonctionne** 
Ouvrir le navigateur à l'adresse `localhost:9000` 






4. Implémenter les modèles 
5. préparer et faire les migrations :    
`python manage.py makemigrations`
`python manage.py migrate` 
ou les lancer depuis le fichier softdesk/commands.migrate_pipenv 
ou lancer le container en décommentant la ligne "command" :    
`docker composer up --build --remove_orphans` 





