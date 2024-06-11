# Bienvenue.

Ce code est un exercice de scraping dans mon cursus d'OpenClassroom dédié à récupérer un certains
nombre d'informations venant du site (de démo) de books.toscrape.com.

Il notera ces données dans plusieurs fichiers csv dans l'arborescence du projet.  
Il téléchargera aussi les images des livres correspondants au même endroit.

### Pour lancer ce projet :

Vous pouvez dans un premier temps télécharger le projet et extraire son zip à l'emplacement de
votre choix.<br>
Copiez son chemin une fois extrait.

Puis, si vous avez Python3 déjà installé :  
Dans un terminal de commandes tel que Bash ou l'invite de commandes cmd.  
Pour vous rendre dans le dossier du projet, vous pouvez y écrire :
```
Sous Bash : cd chemin/du/dossier (ou cd ctrl+shift+inser)
Sous cmd : cd chemin\du\dossier (ou cd ctrl+v)
```

---

Pour initialiser un environnement virtuel appelé ici `.venv`, écrivez : 
```
python -m venv .venv
```
Puis, vous l'activez grâce à  
**sous cmd** :
```
.venv\scripts\activate
```
**sous Bash** :
```
source .venv/scripts/activate
```

---

Maintenant que vous avez activé l'environnement virtuel :  
Pour installer les dépendances, écrire dans la console
```
pip install -r requirements.txt
```

---

Enfin, pour lancer le programme, vous pouvez lancer :
```
python main.py
```