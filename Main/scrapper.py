# Scrapping from reclameaqui.com.br
import os
from multiprocessing import Pool
from scrap import scrap



def scrapper_reclameaqui(empresas : list, n_threads : int = 1):

    # divide a lista de empresas em partes iguais para cada thread
    empresas_divididas = [empresas[i::n_threads] for i in range(n_threads)]

    # cria um diretório para os metadados se não existir
    if not os.path.exists('metadados'):
        os.makedirs('metadados')

    # cria um diretório para os hyperlinks se não existir
    if not os.path.exists('hyperlinks'):
        os.makedirs('hyperlinks')

    # cria um diretório para as reclamações se não existir
    if not os.path.exists('reclamacoes'):
        os.makedirs('reclamacoes')

    
    # criando os subprocessos
    with Pool(n_threads) as pool:

        pool.map(scrap, empresas_divididas)
        print("Scrapping concluído na thread ", os.getpid())
        pool.close()



    





