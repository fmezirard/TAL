# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:30:35 2023
@author: Floriane Mézirard & Lucie Raimbault
"""

# Web Scraping


import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from datetime import datetime


#########################
# Définition de fonction

# Récupération des url pour scraper toutes les pages

def parseURLPage(mon_url):
    # Ouvrir avec openurl mon_url
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(mon_url,headers={'User-Agent':user_agent})
    try: # gestion des exceptions avec un bloc try/except
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e) # sortie du programme avec affichage de l’erreur
    bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml
    page = bsObj.find("ul",class_="_1wkzzau0 _1wkzzau3 a1msqi5a a1msqifq").find_all("a")

    liste_lien_page = [elem.attrs["href"] for elem in page]
    l_lien_sans_doublons = []
    for lien in liste_lien_page:
        if lien not in l_lien_sans_doublons:
            l_lien_sans_doublons.append(lien)

    return l_lien_sans_doublons


# Récupération des url des postes d'une page 

def parseURLPoste(mon_url):
    # Ouvrir avec openurl mon_url
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(mon_url,headers={'User-Agent':user_agent})
    try: # gestion des exceptions avec un bloc try/except
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e) # sortie du programme avec affichage de l’erreur

    bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml
    division_poste = bsObj.find_all("div",class_="_1wkzzau0 a1msqi4y a1msqi4w")
    
    l_lien_poste = [elem.find("a").attrs["href"] for elem in division_poste]
    return l_lien_poste


# Récupération des informations pour un poste

def parseInfoPoste(mon_url):
    # Ouvrir avec openurl mon_url
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(mon_url,headers={'User-Agent':user_agent})
    try: # gestion des exceptions avec un bloc try/except
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e) # sortie du programme avec affichage de l’erreur

    bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml

    titre = bsObj.find("h1").get_text()
    company = bsObj.find("div",class_="_1wkzzau0 a1msqigi a1msqi5a a1msqig2 a1msqifi szurmz2e szurmz2n").find("span",class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuo1 lnocuo21 _1d0g9qk4 lnocuod").get_text()
    lieu_categorie_contrat = bsObj.find_all("span",class_="_1wkzzau0 a1msqi5a")
    l_lieu_categorie_contrat = [elem.get_text() for elem in lieu_categorie_contrat]
    lieu = l_lieu_categorie_contrat[0]
    categorie = l_lieu_categorie_contrat[1]
    contrat = l_lieu_categorie_contrat[2]
    try :
        salaire = l_lieu_categorie_contrat[3]
    except IndexError:
        salaire = None
    parution = bsObj.find_all("span",class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuo1 lnocuo22 _1d0g9qk4 lnocuoa")[-1].get_text()
    description = bsObj.find("div", class_="_1wkzzau0 _1pehz540").get_text()

    # Création d'un dictionnaire pour stocker les résultats
    data = {
        "titre" : titre,
        "entreprise" : company,
        "lieu" : lieu,
        "categorie" : categorie,
        "contrat" : contrat,
        "salaire" : salaire,
        "parution" : parution,
        "description" : description
    }

    try:
        note = bsObj.find("div",class_="_1wkzzau0 a1msqigi a1msqi5a a1msqig2 a1msqifi szurmz2e szurmz2n").find("span",class_="_1wkzzau0 _1jcz3123").get_text()
    except AttributeError:
        note = None
    finally:
        data["note"] = note

    try:
        lien_review = bsObj.find("div",class_="_1wkzzau0 a1msqigi a1msqi5a a1msqig2 a1msqifi szurmz2e szurmz2n").find_all("a")
        try :
            review = [lien.attrs["href"] for lien in lien_review if "reviews" in lien.attrs["href"]][0]
        except IndexError:
            review = None
    except AttributeError:
        review = None
    finally:
        data["review"] = review

    return data




# Programme principal
if __name__ == '__main__':

    # Site à scraper seek
    url = "https://www.seek.com.au"

    # choix d'une catégorie de job
    categorie = "/data-jobs"
    url_site = url + categorie
    l_page_a_scraper = parseURLPage(url_site)

    l_lien_poste = []
    for fin_url in l_page_a_scraper:
        l_lien_poste.extend(parseURLPoste(url+fin_url))

    # liste de dictionnaire
    l_InfoPoste = []
    for fin_url_poste in l_lien_poste:
        l_InfoPoste.append(parseInfoPoste(url+fin_url_poste))

    # transformation en dataframe
    df = pd.DataFrame(l_InfoPoste)
    date = datetime.today().strftime('%Y%m%d')
    df.to_excel(f"{date}-Donnees_Info_Poste.xlsx", index=False)



# Fonction 1
# print(token)
# ['/data-jobs', '/data-jobs?page=2', '/data-jobs?page=3', '/data-jobs?page=4', '/data-jobs?page=5', '/data-jobs?page=6', '/data-jobs?page=7']

# Fonction 2
# print(len(parseURLPoste("https://www.seek.com.au/data-jobs")))
# 59?type=standard', '/job/70954351?type=standout', '/job/70985060?type=standard', '/job/71000164?type=standout', '/job/70995657?type=standout', '/job/70927078?type=standard', '/job/71014942?type=standout', '/job/71025081?type=standout', '/job/71021412?type=standout', '/job/71024802?type=standout']
#url_info_poste = "https://www.seek.com.au/job/70983981?type=standout#sol=51c658af5e39591eb59de73d370c2c993b9b72cd"
#print(parseInfoPoste(url_info_poste))




#########################
#########################
#########################    !!!!!!!!!   A FAIRE  !!!!!!!
######################### 
#########################
# 3 - Si lien de review -- récupérer les commentaires et notes sur l'entreprise
# analyses des pages de review -- exemple avec le liens ci-dessous
# Idées --
#  Faire comme plus haut récupérer le nombre de page (url) à scrapper 
# !!!!!!!!!! le lien pour chaque page est le même ....
# !!!!!!!!!! idee : peut être récupérer le nombre de page et faire du selenium en parallèle pour changer de page ?? je ne sais pas si ca marchera ...
#  pour chaque commentaire récupérer la date + la note + le commentaire ==> sauvegarder les résultats sous forme de dictionnaire comme plus haut


# url_review = "https://www.seek.com.au/companies/australiansuper-813334/reviews?jobId=70983981"


# # ne marche pas
# def parseURLReviewnbrePage(mon_url):
#     # Ouvrir avec openurl mon_url
#     user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     req = Request(mon_url,headers={'User-Agent':user_agent})
#     try: # gestion des exceptions avec un bloc try/except
#         html = urlopen(req)
#     except (HTTPError, URLError) as e:
#         sys.exit(e) # sortie du programme avec affichage de l’erreur
#     bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml

#     page = bsObj.find("nav",class_="ipcm5y0 ipcm5y1")#.find_all("span",class_="ipcm5y0 _2q2j1u8 _2q2j1u4")[1:].get_text()
#     return page

# # à faire
# def parseInfoReview(mon_url):
#     # Ouvrir avec openurl mon_url
#     user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     req = Request(mon_url,headers={'User-Agent':user_agent})
#     try: # gestion des exceptions avec un bloc try/except
#         html = urlopen(req)
#     except (HTTPError, URLError) as e:
#         sys.exit(e) # sortie du programme avec affichage de l’erreur

#     bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml

#     return 

# parseInfoReview(url_review)