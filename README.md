# FusionBrain API

**fusionbrain-api** — это библиотека, предоставляющая удобный интерфейс для взаимодействия с API сайта генерации изображений [FusionBrain](https://fusionbrain.ai/).

## Установка

Установите библиотеку через `pip`:

```sh
pip install git+https://github.com/cardisnotvalid/fusionbrain-api.git
```

## Основные методы

### get_models

Возвращает список доступных моделей для генерации изображений.

### generate

Генерирует изображение на основе текстового запроса. Параметры:

- **prompt** (str): Текстовый запрос для генерации изображения.
- **model_id** (int, по умолчанию 4): Идентификатор модели.
- **width** (int, по умолчанию 1024): Ширина изображения.
- **height** (int, по умолчанию 1024): Высота изображения.

### check_status

Проверяет статус запроса на генерацию изображения. Параметры:

- **request_id** (str): Идентификатор запроса.

### wait_generation

Ожидает завершения генерации изображения. Параметры:

- **request_id** (str): Идентификатор запроса.
- **attempts** (int, по умолчанию 10): Количество попыток проверки статуса.
- **delay** (int, по умолчанию 3): Задержка между проверками статуса в секундах.

## Пример использования

### Синхронный вариант

```python
from fusionbrain import FusionBrainAI
from fusionbrain.utils import save_image_b64

API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"

prompt = "Нарисованный кистью и красками рисунок природы, море, горы, сосны, спокойные цвета"

with FusionBrainAI(API_KEY, SECRET_KEY) as fusion_brain:
    generate = fusion_brain.generate(prompt)
    result = fusion_brain.wait_generation(generate.uuid)

save_image_b64(result.image, "image.png")
```

###  Асинхронный вариант

```python
import asyncio

from fusionbrain import AsyncFusionBrainAI
from fusionbrain.utils import save_image_b64

API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"

prompt = "Нарисованный кистью и красками рисунок природы, море, горы, сосны, спокойные цвета"

async def main() -> None:
    async with FusionBrainAI(API_KEY, SECRET_KEY) as fusion_brain:
        generate = await fusion_brain.generate(prompt)
        result = await fusion_brain.wait_generation(generate.uuid)

save_image_b64(result.image, "image.png")
```

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности см. в файле [LICENSE](LISENCE).
