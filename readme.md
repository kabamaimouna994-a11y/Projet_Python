# API Gestion École

## Description

Ce projet est une API FastAPI pour gérer une école :
- Gestion des classes (création, suppression, liste, détails)
- Gestion des étudiants (ajout, suppression, modification, recherche)
- Gestion des notes et calcul des moyennes
- Statistiques globales

Toutes les fonctionnalités sont disponibles via Postman 

Note importante pour le test
Le projet utilise un dictionnaire Python stocké en mémoire vive (ecole = {}), ce qui signifie que les données sont réinitialisées à chaque redémarrage du serveur.

Pour tester l'API, vous devez commencer par créer une classe.
-