FROM python:3.9.5

# Install Firefox
RUN apt-get update -y && apt-get install -y firefox-esr

# Install Geckodriver
RUN BASE_URL=https://github.com/mozilla/geckodriver/releases/download \
  && VERSION=$(curl -sL https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d '"' -f 4) \
  && curl -sL "$BASE_URL/$VERSION/geckodriver-$VERSION-linux64.tar.gz" | tar -xz -C /usr/local/bin

RUN pip install --upgrade pip

RUN mkdir /upwork-scraper
WORKDIR /upwork-scraper

ADD requirements.txt .
RUN pip install -r requirements.txt --upgrade

COPY . .

ENTRYPOINT ["python", "-m", "upwork"]
# CMD [ "--headless", "--disable-gpu", "--remote-debugging-address=0.0.0.0", "--remote-debugging-port=9222" ]
