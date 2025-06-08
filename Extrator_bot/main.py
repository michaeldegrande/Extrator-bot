from scraper.coletor_pdf import baixar_pdf_cash4life
from scraper.parser_pdf import extrair_resultados_pdf
from scraper.exportar import exportar_para_excel
from scraper.utils import criar_logger
import os
import sys

logger = criar_logger()

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Quando for executável (.exe)
        return os.path.dirname(sys.executable)
    # Quando for script Python comum
    return os.path.dirname(__file__)

def main():
    base_dir = get_base_dir()
    download_dir = os.path.join(base_dir, "downloads")
    os.makedirs(download_dir, exist_ok=True)  # Garante que a pasta existe

    try:
        caminho_pdf = baixar_pdf_cash4life(download_dir)
        df = extrair_resultados_pdf(caminho_pdf)

        if df.empty:
            logger.warning("⚠️ Nenhum resultado extraído do PDF.")
        else:
            caminho_excel = os.path.join(base_dir, "resultados_cash4life.xlsx")
            exportar_para_excel(df, caminho_excel)

    except Exception as e:
        logger.error(f"❌ Erro geral no processo: {e}")

if __name__ == "__main__":
    main()
