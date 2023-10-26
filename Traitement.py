# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 19:40:35 2023
@author: Floriane Mézirard & Lucie Raimbault
"""

"""
Notre jeu de données étant en anglais nous utiliserons la librairy nltk.
"""


import re
import pandas as pd 
import string
from collections import defaultdict
from datetime import datetime

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('stopwords')

from wordcloud import WordCloud
import matplotlib.pyplot as plt


#########################
# Ouverture du fichier

df = pd.read_excel ('20231026-Donnees_Info_Poste.xlsx') 


# Pré-traitement

#########################
# Colonne """parution""" 
df['parution_modif'] = None
for ind, date in enumerate(df.parution) :
    pattern = r'(\d+[dh])'  # Correspond à un nombre suivi de "d" ou "h"
    temps = re.findall(pattern, date)[0]
    df.parution_modif.iloc[ind] = temps



#########################
# Colonne description -- suppression de la ponctuation + lemmatisation ==> recontruction de la description

df['description_modif'] = None
# ponctuation
punct = string.punctuation
# Mots vides
st = set(stopwords.words('english'))
# Racinisation
stemmer = PorterStemmer()


for ind, description in enumerate(df.description):
    # Transformation de la phrase, sans prendre en compte les stopwords, en mot.
    words = [tok.lower() for tok in word_tokenize(description) if tok not in set(st) and tok not in string.punctuation]
    # Racinnation des mots 
    racine = [stemmer.stem(mot) for mot in words]

    df.description_modif.iloc[ind] = " ".join(racine)



###########################
# Nuage de mots pour l'ensemble des textes

# Pour chaque texte compter le nombre de mot -- diconnaire globale contenant les dictionnaires de comptes pour chaque texte

counts_glob = {}

for num, description in enumerate(df.description_modif) : 
    l_mot = description.split()
    counts = {}

    for mot in l_mot:
        counts[mot] = counts.get(mot,0)+1
    
    counts_glob[num] = counts


# Avec le résultat précédent faire un SEUL dictionnaire avec la somme de tous les dictionnaires
# Créez un dictionnaire pour stocker les sommes
sommes = defaultdict(int)

# Parcourez les sous-dictionnaires et ajoutez les valeurs aux mots correspondants
for document in counts_glob.values():
    for mot, valeur in document.items():
        sommes[mot] += valeur

# Convertissez le dictionnaire defaultdict en un dictionnaire ordinaire
resultat = dict(sommes)


# Créez un objet WordCloud
nuage_de_mots = WordCloud(width=800, height=400, background_color='white',max_words=50)

# Générez le nuage de mots à partir du dictionnaire
nuage_de_mots.generate_from_frequencies(resultat)

# Affichez le nuage de mots
plt.figure(figsize=(10, 5))
plt.imshow(nuage_de_mots, interpolation='bilinear')
plt.axis('off')

# Sauvegardez l'image
plt.savefig("nuage_de_mots.jpeg")

plt.show()



# Sauvegarde du nouveau jeu de données modifiés
date = datetime.today().strftime('%Y%m%d')
df.to_excel(f"{date}-Donnees_Info_Poste_Modif.xlsx", index=False)