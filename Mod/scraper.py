# Scrapping from reclameaqui.com.br
import os
from Mod.scrap import scrap

def scraper_reclameaqui(empresas: list):

    # cria diretórios necessários
    os.makedirs('metadados', exist_ok=True)
    os.makedirs('hyperlinks', exist_ok=True)
    os.makedirs('reclamacoes', exist_ok=True)

    scrap(empresas)

    