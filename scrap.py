import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pickle
from multiprocessing import Pool, cpu_count
import pandas as pd
import openpyxl
import unidecode
import requests
import re 

url_review = "https://www.seek.com.au/companies/australiansuper-813334/reviews"
url_api="https://api-seek.prod.companyreview.co/companies/813334/company-reviews?page=1&sort=&api_key=jwt_prodSeekAuBrowserKey"
# ne marche pas
#def company_id(liste_url):


# à faire
# def parseInfoReview(mon_url):
#     # Ouvrir avec openurl mon_url
#     user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     req = Request(mon_url,headers={'User-Agent':user_agent})
#     try: # gestion des exceptions avec un bloc try/except
#         html = urlopen(req)
#     except (HTTPError, URLError) as e:
#         sys.exit(e) # sortie du programme avec affichage de l’erreur

#     bsObj = BeautifulSoup(html, "lxml") # en utilisant le parser de lxml

#     page = bsObj.find_all("span")
#     liste=[elem.get_text() for elem in page]
#     #for text in page:
#     #liste_lien_page = [elem.attrs["href"] for elem in page]

#     return liste

def scrap_review(url):
    id_comp=
    url_api=f"https://api-seek.prod.companyreview.co/companies/{id_comp}/company-reviews?page=1&sort=&api_key=jwt_prodSeekAuBrowserKey"
    response = requests.get(url)
    response_dict = response.json()
    liste=[]
    try :
        reviews = response_dict['data']
        pros=[dico["pros"] for dico in reviews]

    except KeyError: 
        pass
    return pros


a=scrap_review(url_api)

