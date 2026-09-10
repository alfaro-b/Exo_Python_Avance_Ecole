# Gestion d'une école

Exercice réalisé dans le cadre de la formation afin d'apprendre à manipuler les DAO (Data Access Object) et l'accès à une base de données MySQL avec Python.   
Application Python en ligne de commande utilisant une base de données MySQL.

## Fonctionnalités

- Gestion des élèves, enseignants, cours et adresses
- CRUD complet via des DAO
- Affectation d'un enseignant à un cours
- Inscription d'un élève à un cours
- Ajout d'une adresse à un élève ou un enseignant
- Affichage des cours selon l'utilisateur :
  - Élève : cours suivis
  - Enseignant : cours enseignés
  - Directeur : tous les cours

## Architecture


main.py   
   ↓   
School   
   ↓   
DAO   
   ↓   
MySQL   
