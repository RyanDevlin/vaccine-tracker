# vaccine-tracker
scrape turbovax site and alert when there is availability in NYC area

# Setup
```bash
  python3 -m venv venv 
  . venv/bin/activate 
  pip install -rrequirements.txt 

  python setup.py build 
  python setup.py install 
```
# Install GeckoDriver on Linux
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```

# Install GeckoDriver on MacOS
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```