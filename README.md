Aperçu

Ce projet met en œuvre une architecture multi-services conteneurisée avec Docker Compose. Il s'agit d'une stack hybride pilotant simultanément une base de données SQL (MySQL) et une base de données NoSQL (MongoDB), liées par une API développée en FastAPI.

L'application expose des données relatives à la saison 2026 de Formule 1, incluant les profils des pilotes et des actualités techniques sur les nouvelles réglementations.

Architecture
L'infrastructure est composée de cinq services distincts :

db_mongo : Base de données NoSQL utilisant une image personnalisée non-root. Elle stocke les articles et actualités.
db_mysql : Base de données SQL officielle stockant les profils et biographies des pilotes.
admin_mongo : Interface web Mongo Express pour la gestion de la base NoSQL.
admin_mysql : Interface web Adminer (version 4.8.1) pour la gestion de la base SQL.
api : Application FastAPI (Python) servant de passerelle entre les deux bases de données.
Caractéristiques Techniques
Résilience : Politique de redémarrage sur tous les services.on-failure
Orchestration : Gestion stricte des dépendances via des healthchecks. L'API ne démarre que lorsque les deux bases de données sont opérationnelles et peuplées.
Sécurité :
Isolation réseau : Les bases de données ne sont pas exposées sur l'hôte.
Utilisateurs non-root pour les services MongoDB et API.
Gestion des secrets via variables d'environnement ()..env
Healthchecks Métiers : Validation de l'intégrité des données au démarrage (vérification du nombre d'entrées attendues dans les collections et tables).
Installation et Lancement
Prérequis
Docker et Docker Compose installés sur la machine.
Un fichier configuré (se référer au fichier )..env.env.example
Déploiement
Pour initialiser et lancer l'ensemble de la stack :

docker compose up -d --build
Pour réinitialiser complètement les volumes et les données :

docker compose down -v && docker compose up -d
Points d'accès
API FastAPI
Articles F1 (MongoDB) : http://localhost:8000/posts
Pilotes F1 (MySQL) : http://localhost:8000/users
Interface Swagger : http://localhost:8000/docs
Administration
Adminer : http://localhost:8080 (Serveur : db_mysql)
Mongo Express : http://localhost:8081
Pipeline CI/CD
GitHub Actions

Le fichier automatise entièrement le cycle de vie de l'application en trois jobs séquentiels :.github/workflows/main.yml

Job	Rôle	Condition
Job 1 – Build & Security Scan	Construit l'image API, la scanne avec Docker Scout (bloquant sur CRITICAL) et scanne l'image MySQL officielle avec Trivy (informatif)	push / PR sur main
Job 2 – Integration Tests	Déploie la stack complète, attend que tous les services soient healthy, valide les routes et /posts/users	après Job 1
Job 3 – Publish	Publie l'image API sur Docker Hub avec le tag latest	après Job 2
Secrets GitHub requis
Configurer dans Settings → Secrets and variables → Actions :

Secret	Description
DOCKERHUB_USERNAME	Nom d'utilisateur Docker Hub
DOCKERHUB_TOKEN	Access Token Docker Hub (pas le mot de passe)
MYSQL_ROOT_PASSWORD	Mod de passe root MySQL
MONGO_INITDB_ROOT_PASSWORD	Rencontrez la bonne racine MongoDB
Structure du Projet
/api : Code source, Dockerfile et configurations de l'API.
/mongo : Dockerfile non-root et scripts d'initialisation NoSQL.
/sqlfiles : Scripts SQL pour l'initialisation de la base de données pilotes.
docker-compose.yml : Fichier principal d'orchestration.
.github/workflows/main.yml : Actions GitHub du CI/CD du pipeline.
