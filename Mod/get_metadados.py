import os
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def get_metadados(empresa : str) -> None:

    # URL da pagina principal da empresa
    url_p = 'https://www.reclameaqui.com.br/empresa/' + empresa + '/'


    if not os.path.exists(f'metadados/metadados_{empresa}.csv'):
        try:

            driver = uc.Chrome(use_subprocess=True)

            # acessando a pagina principal da empresa
            driver.get(url_p)

            time.sleep(random.randint(2,4))
                
            # ramo de atividade da empresa
            categoria = driver.find_element(By.ID, 'info_segmento_hero').text

            # reputação da empresa
            reputacao = driver.find_element(By.ID, 'tag_reputacao_hero').text

            # sobre a empresa
            sobre = driver.find_element(By.CSS_SELECTOR, 'ul.sc-1915fv4-2.idgfcC').text
            sobre = sobre.split("\n")[0] 

            metadata = {
                'nome': empresa,
                'categoria': categoria,         
                'reputacao': reputacao,         
                'sobre': sobre       
            }

            driver.quit()
            
            metadata_p = pd.DataFrame(metadata, index=[0])
            metadata_p.to_csv(f'metadados/metadados_{empresa}.csv', index=False)

            
        except Exception as e:
            print(e)
            driver.quit()
            os._exit(1)
    
    