# Easy Date
Projet Universitaire

## Cadre du projet

Dans un cadre des cours de programmation Python du Master 2 SISE (Statistiques et informatique pour la science des données) de l’université Lyon 2 lumière il nous est demandé de construire un modèle prédictif performant permettant de comprendre l’influence des variables à partir d’un jeu de données mais aussi de créer une application Dash, hébergée sur Heroku. De plus nous devions afin d’assurer la pérennité du projet concevoir une documentation technique et fonctionnelle.

Ce travail à été réalisé en 21 jours par groupe de 3 étudiants.

## Concept du projet

La base de données utilisée dans le cadre de ce projet provient de la société d’évènement fictive de speed dating EasyDate.
Avant d’organiser les différentes vagues de speed dating, l’entreprise récolte les informations de tous les participants. A l’issue des rencontres chaque participant décide si oui ou non il souhaite revoir la personne rencontrée. Malheureusement le taux de match est faible, ce qui fait perdre beaucoup de temps et d’argent à l’entreprise.

Afin de maximiser son temps et accroître ses bénéfices, EasyDate a décidé de recourir à son équipe de data scientist en leur demande de construire un modèle permettant de prédire si deux personnes vont matcher selon le formulaire compléter avant la rencontre. Un modèle à déjà été construit mais il n’est pas très fiable, elle a donc créé une compétition Kaggle pour que les étudiants de SISE puissent à leur tour proposer un modèle de scoring plus performant pour prédire si l’amour va opérer entre deux personnes. 

## Language utilisées

Code :

- Python
 
Application : 

- Dash

Publication sur le web :

 - Render

## Lien de l'application

https://ai-match.onrender.com/

## Repository

L'application se découpe en 2 parties :

 - La partie Machine Learning :
   2 fichiers .py s'occupent de cette partie, le premier Nettoyage_Donnee.py qui s'occupent de nettoyer les données brutes.
   Le second Model.py s'occupe de la création du modèle créé pour la prédiction (utilisation KNN).
   
 - La partie Application :
   2 fichiers .py s'occupent de cette partie, le premier Dash_function.py permet de créer les fonctions et les variables utilisées pour l'application et les graphiques.
   Le second easymatch.py est le main pour l'application DASH du reporting.
   
Il existe 3 dossiers qui stockent les images et les données utilisées ainsi que les docs.
