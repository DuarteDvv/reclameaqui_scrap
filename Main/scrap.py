
from get_metadados import get_metadados
from get_hyperlinks import get_hyperlinks
from get_reclamacoes import get_reclamacoes

def scrap(empresas : list):

    for empresa in empresas:

       
        # pegando metadados da empresa (nome, categoria, reputação, sobre)
        get_metadados(empresa)
        print(f"Metadados da empresa {empresa} salvos com sucesso.")

        # pegando hyperlinks das reclamações da empresa (nome, categoria, reputação, sobre)
        hyperlinks = get_hyperlinks(empresa)
        print(f"Hyperlinks da empresa {empresa} salvos com sucesso.")

        # pegando reclamações da empresa (nome, categoria, reputação, sobre)
        get_reclamacoes(empresa, hyperlinks)
        print(f"Reclamações da empresa {empresa} salvas com sucesso.")

        print(f"Scrapping da empresa {empresa} concluído.")
        print("-----------------------------------------------------")



