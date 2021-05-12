# Upwork Scraper

## Installation
- Requirements:
  * Python >= 3.9.0
  * Chrome or Chromium
  * [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) in your $PATH
```bash
git clone https://github.com/lucasrcezimbra/upwork-scraper
cd upwork-scraper
python -m venv .venv
```

### To use
```bash
# Install requirements
pip install -r requirements.txt
# Run help to see how to use
python -m upwork --help
```

### For development
```bash
# Install requirements-dev
pip install -r requirements-dev.txt
# Install pre-commit
pre-commit install
# Run tests
pytest
# Run with DEBUG and HEADLESS to facilitate development
DEBUG=True HEADLESS=False python -m upwork --help
```
