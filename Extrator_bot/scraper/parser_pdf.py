import pdfplumber
import pandas as pd
import re
from scraper.utils import criar_logger

logger = criar_logger()

def extrair_resultados_pdf(caminho_pdf: str) -> pd.DataFrame:
    logger.info(f"Iniciando extração do PDF com pdfplumber: {caminho_pdf}")

    resultados = []

    # Regex que captura a data e 5 dezenas seguidas de 'CB' e o número da Cash Ball
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{2})\s+(\d{1,2})-\s*(\d{1,2})-\s*(\d{1,2})-\s*(\d{1,2})-\s*(\d{1,2})\s+CB\s+(\d+)"
    )

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                texto = page.extract_text()
                if not texto:
                    continue

                linhas = texto.split('\n')
                for linha in linhas:
                    # Captura múltiplas partidas por linha com regex
                    matches = pattern.findall(linha)
                    for match in matches:
                        data = match[0]
                        dezenas_originais = [int(num) for num in match[1:6]]
                        dezenas_ordenadas = sorted(dezenas_originais, reverse=True)

                        resultados.append({
                            "Data": data,
                            "Dezena 1": dezenas_ordenadas[0],
                            "Dezena 2": dezenas_ordenadas[1],
                            "Dezena 3": dezenas_ordenadas[2],
                            "Dezena 4": dezenas_ordenadas[3],
                            "Dezena 5": dezenas_ordenadas[4]
                        })

        if not resultados:
            logger.warning("⚠️ Nenhum resultado extraído do PDF.")
            return pd.DataFrame()

        df = pd.DataFrame(resultados)

        logger.info("Datas extraídas (antes da conversão):")
        logger.info(df["Data"].tolist())

        # Conversão e ordenação das datas
        df["Data"] = pd.to_datetime(df["Data"], format="%m/%d/%y", errors='raise', dayfirst=False)
        df = df.sort_values(by="Data", ascending=True).reset_index(drop=True)

        logger.info("Datas ordenadas (após conversão):")
        logger.info(df["Data"].dt.strftime("%d/%m/%Y").tolist())

        # Formatando a data final para padrão brasileiro DD/MM/AAAA
        df["Data"] = df["Data"].dt.strftime("%d/%m/%Y")

        logger.info(f"✅ Extração finalizada com {len(df)} resultados válidos.")
        return df

    except Exception as e:
        logger.error(f"❌ Erro ao extrair dados do PDF: {e}")
        return pd.DataFrame()
