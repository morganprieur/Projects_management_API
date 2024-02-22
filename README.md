
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


4. Création du projet Django 

41. **Utilisation de Docker** 
411. Builder le container : 
412. Dans compose.yaml, commenter la ligne "command..." 
413. Lancer la commande :    
`[sudo]* docker compose run <web>* django-admin startproject <nom_projet>* .` 
pour installer le projet Django. 
*: 
sudo : selon votre configuration 
web : le nom du dossier contenant le Dockerfile 
nom_projet : le nom du projet à créer 
. : le dossier courant 

42. **Sans Docker** 
Lancer la commande :    
`django-admin startproject <nom_projet>* .` 
*nom_projet: le nom du projet à créer 


5. **Etapes BDD Django** 
Changer les données dans DATABASES du fichier settings.py en remplaçant les données Sqlite3 par celles-ci :    
```python 
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('POSTGRES_DB'),   # nom de la bdd 
    'USER': os.environ.get('POSTGRES_USER'),
    'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'HOST': '<db>',   # nom du service 
    'PORT': 5432, 
``` 


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

**Pour l'instant les migrations ne sont pas faites** 
On les fera après avoir implémenté les modèles. 



================ 


4. Implémenter les modèles 
5. préparer et faire les migrations :    
`python manage.py makemigrations`
`python manage.py migrate` 
ou les lancer depuis le fichier softdesk/commands.migrate_pipenv 
ou lancer le container en décommentant la ligne "command" :    
`docker composer up --build --remove_orphans` 

================ 

## Créer un groupe 
(Leçon OCR)[https://openclassrooms.com/fr/courses/7192426-allez-plus-loin-avec-le-framework-django/7388713-attribuez-des-permissions-en-utilisant-les-groupes]




## Tests 

*  Emplacement du fichier de test :    
`api/users/tests.py`    

*  Lancer les tests :     
`python manage.py test users.tests -v 3` 
Régler la quantité de détails avec `-v` : `3` = le maximum    




