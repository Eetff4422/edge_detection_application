EdgeDetector
EdgeDetector est un script Python qui permet de détecter les bords dans des images et des vidéos en utilisant l'algorithme de détection de bords de Canny. Il prend en charge les formats d'images .jpg, .png et les vidéos .mp4. Le script parcourt les dossiers, traite les fichiers dans le dossier input et enregistre les résultats dans le dossier output.

Fonctionnalités
Détection de bords dans des images (.jpg, .png)
Détection de bords dans des vidéos (.mp4)
Création automatique des dossiers de sortie si nécessaire
Affichage du temps de traitement pour chaque fichier
Installation
Clonez le dépôt :

bash
Copy code
git clone <URL_DU_DEPOT>
cd EdgeDetector
Installez les dépendances requises :

bash
Copy code
pip install opencv-python
Utilisation
Placez vos fichiers d'images et de vidéos dans le dossier data/input.

Configurez les paramètres de détection de bords dans le script (seuils threshold1 et threshold2).

Exécutez le script :

bash
Copy code
python edge_detector.py
Exemple
css
Copy code
data/
└── input/
    ├── image1.jpg
    ├── image2.png
    └── video1.mp4
Après exécution, les fichiers traités seront sauvegardés dans le dossier data/output correspondant.

Paramètres
data_folder : Chemin du dossier contenant les fichiers à traiter (par défaut "data").
threshold1 : Premier seuil pour l'algorithme de Canny (par défaut 100).
threshold2 : Deuxième seuil pour l'algorithme de Canny (par défaut 200).
Exemple de sortie
Pour une image : data/output/image1.jpg
Pour une vidéo : data/output/video1.mp4
Auteur
Franklin Essono
