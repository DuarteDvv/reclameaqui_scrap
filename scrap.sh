#!/bin/bash

# ativa o ambiente virtual
source /home/luis/Documentos/reclameaqui_scrap/venv/bin/activate

# loop infinito para reiniciar o script caso falhe
while true; do
    echo "Iniciando scraping..." >> /home/luis/Documentos/scrap.log

    /home/luis/Documentos/reclameaqui_scrap/venv/bin/python /home/luis/Documentos/reclameaqui_scrap/scrap_script.py

    echo "O script falhou. Reiniciando em 60 segundos..." >> /home/luis/Documentos/scrapError.log
    sleep 300

done
