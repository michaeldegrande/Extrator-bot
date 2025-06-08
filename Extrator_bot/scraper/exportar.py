import pandas as pd
from scraper.utils import criar_logger

logger = criar_logger()

def exportar_para_excel(df, caminho_arquivo):
    try:
        df.to_excel(caminho_arquivo, index=False)
        logger.info(f"Arquivo Excel salvo: {caminho_arquivo}")
    except Exception as e:
        logger.error(f"Erro ao salvar Excel: {e}")

