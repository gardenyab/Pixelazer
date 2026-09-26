<div align="center">

# Pixelazer

**A Pixelazer-based, fast, and secure Telegram userbot.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

[Features](#features) • [Quick Start](#quick-start)

</div>

---

## Features

- **Performance**: Fast startup time and low memory footprint.
- **Compatibility**: Supports Hikka, FTG, and GeekTG modules.
- **Interactive UI**: Native support for inline buttons, forms, and galleries.
- **Security**: Advanced API call filtering and session protection.

---

## Quick Start

### Prerequisites
- **Python 3.10+**
- Telegram API credentials (`api_id` and `api_hash`) from [my.telegram.org](https://my.telegram.org)

### Installation (Linux / macOS / WSL)

```bash
# Clone the repository
git clone https://github.com/gardenyab/Pixelazer && cd Pixelazer

# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and run
pip install -r requirements.txt
python3 -m pixelazer