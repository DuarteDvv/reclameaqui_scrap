import os
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def get_hyperlinks(empresa : str) -> list:
    

    # URL da pagina de reclamações da empresa
    def url_r(page : int, type : str = 'EVALUATED') -> str:

        # https://www.reclameaqui.com.br/empresa/temu/lista-reclamacoes/?pagina=1&status=EVALUATED
        return 'https://www.reclameaqui.com.br/empresa/' + empresa + '/lista-reclamacoes/?pagina='+ str(page) +'&status=' + type

    # pegando hyperlinks das reclamações avaliadas e/ou respondidas
    all_hyperlinks = []

    Numero_de_paginas = 50 # máximo

    # Se o CSV ainda não existe, inicia a coleta
    if not os.path.exists(f'hyperlinks/hyperlinks_{empresa}.csv'):
    
        for i in range(Numero_de_paginas):

            driver = uc.Chrome(use_subprocess=True)

            try:
                
                
                driver.get(url_r(page=i + 1, type='EVALUATED'))
                
                time.sleep(random.randint(2, 5))
                
                
                # Captura os hyperlinks da página atual
                div_hyperlinks = driver.find_elements(By.CSS_SELECTOR, 'div.sc-1pe7b5t-0.eJgBOc')
                current_hyperlinks = [h.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for h in div_hyperlinks]
                
                if not current_hyperlinks:
                    print("Nenhum hyperlink encontrado")
                    driver.quit()
                    break

                print(f"Página {i+1} - hyperlinks: {current_hyperlinks}")
                all_hyperlinks += current_hyperlinks

                driver.quit()

                
            except Exception as e:
                print(e)
                driver.quit()
                os._exit(1)
              


        df = pd.DataFrame(all_hyperlinks, columns=["Hyperlinks"])
        df.to_csv(f'hyperlinks/hyperlinks_{empresa}.csv', index=False)
        all_hyperlinks = df["Hyperlinks"].tolist()
        
    else:
        
        # Se o CSV já existe, apenas o lê
        df = pd.read_csv(f'hyperlinks/hyperlinks_{empresa}.csv')
        all_hyperlinks = df["Hyperlinks"].tolist()

    return all_hyperlinks
