<div align="center">

# Pixelazer

**Быстрый и безопасный Telegram юзербот на базе Pixelazer.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

[Возможности](#возможности) • [Быстрый старт](#быстрый-старт)

</div>

---

## Возможности

- **Производительность**: Быстрый запуск и низкое потребление памяти.
- **Совместимость**: Поддержка модулей Hikka, FTG и GeekTG.
- **Интерактивный интерфейс**: Нативная поддержка инлайн-кнопок, форм и галерей.
- **Безопасность**: Продвинутая фильтрация вызовов API и защита сессий.

---

## Быстрый старт

### Требования
- **Python 3.10+**
- API Telegram (`api_id` и `api_hash`) с сайта [my.telegram.org](https://my.telegram.org)

### Установка (Linux / macOS / WSL)

```bash
# Клонирование репозитория
git clone https://github.com/gardenyab/Pixelazer && cd Pixelazer

# Создание и активация виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей и запуск
pip install -r requirements.txt
python3 -m pixelazer