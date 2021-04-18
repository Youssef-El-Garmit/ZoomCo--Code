# ZoomCo--Code

Bot permettant de se connecter automatiquement aux réunions Zoom. Programmé en Python avec Tkinter.


Explication du code :

-Le script principale est ZoomCo.py, il contient l'interface Tkinter à partir de laquelle on peut programmer une connexion.

-Le script ListProg.py est un dictionnaire qui contient l'ensemble des programmation prévus.

-Le script AutomateZoomCo.py est une boucle infinie qui détecte si l'heure d'une programmation est arrivée.


Mode d'emploi :

Pour que se script fonctionne, il faut au préalable avoir téléchargé l'application Zoom et être connecté.

Pour programmer une connexion, exécuté le script ZoomCo.py. Il vous sera alors demandé de rentrer le lien Zoom ou le numéro et mot de passe de la réunion, ainsi que le la date et l'heure de connexion prevu. Vous pouvez également entrer une durée de connexion au terme de laquelle l'application Zoom se fermera. Un titre de réunion est également demandé. Enfin cliquer sur le bouton "Programmer" pour programmer la réunion. Un message s'affiche alors pour vous confirmer la programmation. 

Pour que la connexion automatique se fasse vous devez IMPERATIVEMENT activer l'automatisation, il s'agit du bouton en haut a gauche, qui doit être vert. Vous pouvez également annuler des programmations directement depuis le "calendrier des programmations" en haut à droite de l'interface. Il suffit de cliquer sur ce dernier et sélectionner les programmations à annuler.

Vous pouvez ainsi fermer l'interface et continuer vos activités, et ZoomCo se connectera automatiquement aux dates indiquées. 


ATTENTION : À chaque redémarrage l'activation est désactivé il faut donc l'activer manuellement.
