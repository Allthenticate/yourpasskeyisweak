# Automated Chrome Phishing Tool

This tool is meant as a proof-of-concept only and is not intended to be a weaponized exploit. However, this PoC should make it clear that it would not be hard to scale and weaponize such an attack. We have outlined the next steps required below.

## Novel insight
Historic phishing attacks would simply target phishing the credentials and storing them to be used at a later time. 
This attack actively emulates keyboard presses into a Chrome instance directly in a high-fidelity way to ensure a 
success login to the browser, which will then sync **ALL** of victims passwords and passkeys. While passkeys do require 
an additional PIN, the page that this is entered into, is itself a phishable webpage that is also a part of this PoC.

## Attack chain
1. Launch this phisher
2. Convince a victim to browse to your page
3. Watch the machine take over and steal their credentials
4. Launch Chrome with the specific user directory (e.g., `/tmp/pHish3d`)at any point to become that user


## Path to weaponization
1. Read the output from the local Chrome browser to display relevant content to the victim, ensuring a successful phish everytime
2. Incorporate multiple instances to scale the attack
3. Tie tool in with something like [evilnginx2](https://github.com/kgretzky/evilginx2) to make the attack more convincing
4. Decrypt and export the passkeys to remove the dependence on needing Chrome to use the credentials
5. Automatically detect their IP geolocation and dynamically reconfigure a VPN to appear at the same location
6. Survive sessions post phish to make the attack invisible


# Defense
Use device-bound keys for now.


# Installation & Usage

Getting this running on your Linux machine should be as easy as
```bash
./get_started.sh
```
to install your dependencies and then
```bash
poetry run python passkeyphisher.py
```
to run the phishing attack.

Because the attack will control your local computer, it is best to use a different computer for the victim's browser. [ngrok](https://ngrok.com/downloads/linux) is a nice tool for facilitating this:
```
ngrok http 5000
```

