# Scrapping from reclameaqui.com.br
import pandas as pd
import time
import random
import os
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import setuptools._distutils


empresas_totoal = pd.read_csv('empresas_total.csv')
empresas = empresas_totoal['Nome'].tolist()

e = ['malibu']

for empresa in e:

    # URL da pagina principal da empresa
    url_p = 'https://www.reclameaqui.com.br/empresa/' + empresa + '/'

    # URL da pagina de reclamações da empresa
    def url_r(page : int, type : str = 'EVALUATED') -> str:

        # https://www.reclameaqui.com.br/empresa/temu/lista-reclamacoes/?pagina=1&status=EVALUATED
        return 'https://www.reclameaqui.com.br/empresa/' + empresa + '/lista-reclamacoes/?pagina='+ str(page) +'&status=' + type



    # pegando metadados da empresa (nome, categoria, reputação, sobre)
    if not os.path.exists(f'metadados/metadados_{empresa}.csv'):
        try:

            driver = uc.Chrome()

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
            
        except: 
            driver.quit()
            os._exit(1)

    else:
    
        metadata = pd.read_csv(f'metadados/metadados_{empresa}.csv')
        metadata = metadata.to_dict(orient='records')[0]
    
    
    print(metadata)


   


    # pegando hyperlinks das reclamações avaliadas e/ou respondidas

    all_hyperlinks = []
    
    Numero_de_paginas = 50 # máximo

    # Se o CSV ainda não existe, inicia a coleta
    if not os.path.exists(f'hyperlinks/hyperlinks_{empresa}.csv'):
    
        for i in range(Numero_de_paginas):

            try:
                driver = uc.Chrome()
                
                driver.get(url_r(page=i + 1, type='EVALUATED'))
                
                time.sleep(random.randint(2, 4))
                
                
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
                driver.quit()
                os._exit(1)
              


        df = pd.DataFrame(all_hyperlinks, columns=["Hyperlinks"])
        df.to_csv(f'hyperlinks/hyperlinks_{empresa}.csv', index=False)
        all_hyperlinks = df["Hyperlinks"].tolist()
        
    else:
        
        # Se o CSV já existe, apenas o lê
        df = pd.read_csv(f'hyperlinks/hyperlinks_{empresa}.csv')
        all_hyperlinks = df["Hyperlinks"].tolist()

    print(all_hyperlinks)
    

    
    # pegando dados das reclamações respondidas

    if not os.path.exists(f'reclamacoes/reclamacoes_{empresa}.csv'):

        driver = uc.Chrome()
    
        reclamacoes = []
        #for link in all_hyperlinks:
        for link in all_hyperlinks:
            
            links_coletados = set()
            
            if link in links_coletados:
                continue
            
            links_coletados.add(link)
            
            try:
                driver.get(link)

                time.sleep(random.randint(4, 5))

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

                reclamacoes.append(reclamacao)
                
                print(reclamacao)
                
            except:
                
                driver.quit()
                os._exit(1)


        driver.quit()
 
            
        # transformando em csv as reclamações
        df = pd.DataFrame(reclamacoes)
        df.to_csv(f'reclamacoes/reclamacoes_{empresa}.csv', index=False)
            

    else: 
        
        df = pd.read_csv(f'reclamacoes/reclamacoes_{empresa}.csv')
        reclamacoes = df.to_dict(orient='records')
                
    
    print(reclamacoes)


