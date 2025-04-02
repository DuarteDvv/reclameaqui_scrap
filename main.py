import Mod.scraper as sc 
import argparse
import pandas as pd

def main():

    parser = argparse.ArgumentParser(description="Processa um arquivo CSV.")
    parser.add_argument("-a", "--arquivo", type=str, required=True, help="Nome do arquivo CSV")

    args = parser.parse_args()

    print(f"Arquivo: {args.arquivo}")

    empresas = pd.read_csv(args.arquivo)
    empresas = empresas['Nome'].tolist()

    print(f'{len(empresas)} empresas carregadas com sucesso' )

    sc.scraper_reclameaqui(empresas)

    print("Scrapping concluído")



if __name__ == "__main__":
    main()
    