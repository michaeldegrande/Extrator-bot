import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PDF_FILENAME = "cash4life_historico.pdf"

def baixar_pdf_cash4life(download_dir):
    logging.info("Iniciando o processo de download do PDF do Cash4Life...")

    os.makedirs(download_dir, exist_ok=True)

    # Configurações do Chrome para download automático
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.flalottery.com/cash4life")

    try:
        logging.info("Página carregada, buscando link do PDF do Cash4Life...")

        link = driver.find_element(By.XPATH, "//a[contains(@href, 'c4l.pdf')]")
        pdf_url = link.get_attribute("href")
        logging.info(f"Link do PDF encontrado: {pdf_url}")

        link.click()
        logging.info("Aguardando o término do download...")

        caminho_esperado = os.path.join(download_dir, "c4l.pdf")
        timeout = 30
        tempo_inicial = time.time()

        while not os.path.exists(caminho_esperado):
            if time.time() - tempo_inicial > timeout:
                raise Exception("Download não foi concluído dentro do tempo esperado.")
            time.sleep(1)

        caminho_final = os.path.join(download_dir, PDF_FILENAME)

        # ✅ Remove o arquivo antigo se já existir
        if os.path.exists(caminho_final):
            os.remove(caminho_final)

        os.rename(caminho_esperado, caminho_final)

        logging.info(f"PDF baixado com sucesso: {caminho_final}")
        return caminho_final

    except Exception as e:
        logging.error(f"Erro ao baixar PDF com Selenium: {e}")
        raise
    finally:
        driver.quit()
