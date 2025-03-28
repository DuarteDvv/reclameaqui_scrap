import os
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def get_reclamacoes(empresa : str, all_hyperlinks : list) -> None:

    # pegando dados das reclamações 
    if not os.path.exists(f'reclamacoes/reclamacoes_{empresa}.csv'):

        n_coletadas = 0       

    else: 
        
        df = pd.read_csv(f'reclamacoes/reclamacoes_{empresa}.csv')
        n_coletadas = df.shape[0]

    driver = uc.Chrome()
    
    get_reclamacoes(driver, empresa, all_hyperlinks, n_coletadas)

    driver.quit()

def get_reclamacoes(driver : uc.Chrome , empresa : str, all_hyperlinks : list, n_coletadas : int) -> None:

    for link in all_hyperlinks[n_coletadas:]:
            
        links_coletados = set()
        
        if link in links_coletados:
            continue
        
        links_coletados.add(link)
        
        try:
            driver.get(link)

            time.sleep(random.randint(7, 10))

            titulo = driver.find_element(By.CSS_SELECTOR, '[data-testid="complaint-title"]').text
            lugar = driver.find_element(By.CSS_SELECTOR, '[data-testid="complaint-location"]').text
            data = driver.find_element(By.CSS_SELECTOR, '[data-testid="complaint-creation-date"]').text
            reclamacao_id = driver.find_element(By.CSS_SELECTOR, '[data-testid="complaint-id"]').text
            
            reclamacao_id = (reclamacao_id.split('ID: ')[1])

            parsed_data = time.strptime(data, '%d/%m/%Y às %H:%M')

            reclamacao_base = driver.find_element(By.CSS_SELECTOR, '.sc-lzlu7c-17.fRVYjv').text
            interacoes = driver.find_elements(By.CSS_SELECTOR, '[data-testid="complaint-interaction"]')

            interacoes_text = [i.text for i in interacoes]

            again = driver.find_element(By.CSS_SELECTOR, '.sc-uh4o7z-0.bprQlw:nth-child(2) > div').text
            rating = driver.find_element(By.CSS_SELECTOR, '.sc-uh4o7z-0.bprQlw:nth-child(3) > div').text
            status = driver.find_element(By.CSS_SELECTOR, '[data-testid="complaint-status"]').text

            rating = int(rating.split()[0])
            again = again == 'Sim'

            reclamacao = {
                'id': reclamacao_id,
                'titulo': titulo,
                'lugar': lugar,
                'data': parsed_data,
                'reclamacao_base': reclamacao_base,
                'interacoes': interacoes_text,
                'rating': rating,
                'again': again,
                'status': status
            }


            nova_reclamacao = pd.DataFrame([reclamacao])
            nova_reclamacao.to_csv(f'reclamacoes/reclamacoes_{empresa}.csv', mode='a', index=False, header= not os.path.exists(f'reclamacoes/reclamacoes_{empresa}.csv'))
            
            print(f"Reclamação {reclamacao_id} - Título: {titulo} | Coletada com sucesso!")
            
            
        except Exception as e:
            print(e)
            driver.quit()
            os._exit(1)

   