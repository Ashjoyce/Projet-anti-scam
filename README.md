## 🤖 Auteur
Joyce Ashley MASSAH NSANGOU

# 🎙️ Projet Michel Casper – L'IA anti-arnaque téléphonique

Michel Casper est une intelligence artificielle conçue pour **faire perdre du temps aux arnaqueurs téléphoniques** en simulant une conversation crédible et interactive.

## 🚀 Fonctionnalités

- 🧠 **Réponses générées par IA (LLM)** : Michel comprend et répond naturellement à l’arnaqueur.
- 🗣️ **Synthèse vocale (TTS)** : La voix générée est fluide et personnalisée avec des pauses, hésitations, et effets réalistes.
- 🧏‍♂️ **Reconnaissance vocale (ASR)** : L'IA comprend ce que dit l'arnaqueur en temps réel.
- 🎭 **Simulation d’émotions** : Réagit selon le ton de l’arnaqueur (stress, colère, confusion…).
- 🌀 **Lapsus & hésitations** : Rends la conversation plus crédible et humaine.
- 🧾 **Historique de conversation** : Enregistre les échanges dans des fichiers de log.

## 🛠️ Stack technique

- **Python**
- **Flask + Flask-SocketIO** (interface Web interactive)
- **Google Cloud Speech-to-Text** (reconnaissance vocale)
- **Google Cloud Text-to-Speech (SSML)** (voix réaliste)
- **Nebius InferenceClient** (pour interroger un LLM, ex. Qwen-2)
- **WebSocket / Frontend JS** (communication temps réel)

---

## 🔧 Installation

1. **Clone le dépôt** :
   " bash
git clone https://github.com/Ashjoyce/Projet-anti-scam.git
cd Projet-anti-scam "

3. **Crée un environnement virtuel** :
   python -m venv .venv
source .venv/bin/activate  # (ou .venv\Scripts\activate sous Windows)

4. **Installe les dépendances** :
   pip install -r requirements.txt
   
5. **Ajoute ton fichier key.json dans le dossier (non versionné par Git)** :
   ⚠️ Ne jamais push ce fichier ! Il contient tes clés Google Cloud.

## ▶️ Lancer l'application
 
  Le code est structuré en deux partie : 
  
1. Fichier « anti-scam-1.py » : Il contient le code destiné à l'exécution côté vocal, via le terminal.

2. Fichier « anti-scam.py » :Ce fichier contient le code destiné à l'exécution côté front, via une interface web. Toutefois, toutes les actions et traces sont également référencées dans le terminal. De plus, pour suivre l'historique des échanges, toutes les conversations sont enregistrées dans le fichier « conversation.log ».

  **Version Web (interface en temps réel)** :
   
   Si vous exécutez la partie web avec l'interface, c'est-à-dire le fichier « anti-scam.py », vous pouvez le faire en utilisant la commande suivante dans le terminal : "python anti-scam.py "

   Ensuite, pour accéder à l'interface web, il vous suffit de consulter le fichier « conversation.log » dans lequel vous trouverez un message indiquant « Running on http://127.0.0.1:5000 », ce qui signifie que l'application est en cours d'exécution en local. Vous n'aurez plus qu'à cliquer sur ce lien pour accéder à l'interface.

   Par ailleurs, une note vocale de la réponse du bot IA est générée directement dans le répertoire racine du projet, sous le nom « output.mp3 », afin de vous permettre d'écouter la réponse vocale.

 **Version Terminal (interactive audio uniquement)** :
   " python anti-scam-1.py "

## 📁 Structure du projet

├── anti-scam.py          # Version Web interactive
├── anti-scam-1.py        # Version terminale
├── static/               # Fichiers JS, CSS
├── templates/            # Interface HTML (Flask)
├── logs/                 # Conversations enregistrées
├── key.json              # Clé Google Cloud (ne pas push)
└── .venv/                # Environnement virtuel (exclu de Git)

## 🛡️ Sécurité

✅ Clé API non incluse dans le dépôt

✅ .gitignore configuré pour ignorer les fichiers sensibles

✅ Push protégé par GitHub Secret Scanning

## Objectif
Ce projet a été conçu à des fins pédagogiques et éthiques, pour lutter contre les escroqueries téléphoniques en mobilisant des outils d’IA modernes.
Michel Casper ne remplace pas la vigilance, mais il détourne l’attention des arnaqueurs.

## 📜 Licence
Ce projet est open-source sous licence MIT.
