# Upwork Scraper

## Installation
- Requirements:
  * Python >= 3.9.0
  * [Chrome](https://www.google.com/chrome/)
  * [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) in your $PATH
```bash
git clone https://github.com/lucasrcezimbra/upwork-scraper
cd upwork-scraper
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
# Run help to see how to use
python -m upwork --help
```

### Use in your code
```python
from upwork import Upwork

upwork = Upwork(username='username', password='password', secret_answer='secret_answer')
upwork.login()
userdata = upwork.userdata()
profile = upwork.profile()

```
### Development
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
