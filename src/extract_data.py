import requests
import json
import logging

from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def extract_weather_data(url: str) -> list:
    try:
        logging.info('Iniciando extração dos dados meteorológicos...')

        response = requests.get(url, timeout=(10, 30))

        response.raise_for_status()

        data = response.json()

        if not data:
            logging.warning('Nenhum dado retornado pela API!')
            return []

        output_path = (
            Path(__file__).resolve().parent.parent
            / 'data'
            / 'weather_data.json'
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logging.info(f'Arquivo salvo em: {output_path}')

        return data

    except requests.exceptions.Timeout:
        logging.error('A API demorou demais para responder!')
        raise

    except requests.exceptions.RequestException as error:
        logging.error(f'Erro na requisição: {error}')
        raise

    except ValueError as error:
        logging.error(f'Erro ao interpretar o JSON: {error}')
        raise