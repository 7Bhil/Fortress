# 🔐 Outil de Chiffrement Avancé

Framework cryptographique moderne avec interface en ligne de commande pour le chiffrement/déchiffrement sécurisé de fichiers.

## 🚀 Fonctionnalités

### Algorithmes de chiffrement supportés
- **AES-GCM avec Argon2** - Chiffrement moderne avec authentification intégrée
- **AES-CBC avec HMAC** - Standard éprouvé avec authentification séparée  
- **ChaCha20-Poly1305** - Alternative rapide à AES, idéale pour mobile

### Outils de sécurité
- **Analyseur de force de mots de passe** - Évalue la robustesse des mots de passe
- **Tests d'attaques simulées** - Force brute et dictionnaire
- **Validation d'intégrité** - Vérification que les fichiers n'ont pas été modifiés
- **Génération de clés** - Clés AES et RSA sécurisées

### Interface utilisateur
- **CLI complète** - Interface en ligne de commande intuitive
- **Affichage coloré** - Messages formatés avec codes couleur
- **Progression en temps réel** - Suivi des opérations longues
- **Aide intégrée** - Documentation accessible via `--help`

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Vérification de l'installation
```bash
python main.py --help
```

## 🎯 Utilisation

### Commandes de base

#### Chiffrer un fichier
```bash
python main.py encrypt -f document.pdf -m aes-gcm-argon2
```

#### Déchiffrer un fichier
```bash
python main.py decrypt -f document.pdf.enc
```

#### Lister les méthodes disponibles
```bash
python main.py list-methods
```

#### Analyser un fichier chiffré
```bash
python main.py analyze -f document.pdf.enc
```

### Options avancées

#### Chiffrement avec paramètres personnalisés
```bash
python main.py encrypt -f document.pdf -m aes-gcm-argon2 \
  --memory-cost 131072 --time-cost 4 --parallelism 8
```

#### Spécifier un fichier de sortie
```bash
python main.py encrypt -f document.pdf -m aes-cbc-hmac -o fichier_chiffre.enc
python main.py decrypt -f fichier_chiffre.enc -o document_dechiffre.pdf
```

#### Génération de clés
```bash
# Clé AES
python main.py generate-key -t aes -s 32 -o ma_cle

# Paire de clés RSA
python main.py generate-key -t rsa -s 2048 -o ma_cle_rsa
```

#### Test de force de mot de passe
```bash
python main.py password-strength --check
```

## 🔒 Méthodes de chiffrement

### AES-GCM avec Argon2
- **Niveau de sécurité**: Très élevé
- **Utilisation**: Fichiers sensibles, stockage à long terme
- **Caractéristiques**: 
  - Authentification intégrée (AEAD)
  - Protection contre les attaques par force brute (Argon2)
  - Résistance à la modification des données

### AES-CBC avec HMAC
- **Niveau de sécurité**: Élevé
- **Utilisation**: Compatibilité avec systèmes existants
- **Caractéristiques**:
  - Standard éprouvé et largement utilisé
  - Authentification séparée (HMAC-SHA256)
  - Compatible avec de nombreux systèmes

### ChaCha20-Poly1305
- **Niveau de sécurité**: Très élevé
- **Utilisation**: Applications mobiles, performance critique
- **Caractéristiques**:
  - Très rapide sur processeurs modernes
  - Résistant aux attaques par timing
  - Excellent pour les appareils mobiles

## 🛡️ Sécurité

### Bonnes pratiques
- Utilisez des mots de passe forts (12+ caractères, majuscules, chiffres, symboles)
- Ne réutilisez pas les mêmes mots de passe
- Stockez les fichiers chiffrés dans un endroit sécurisé
- Vérifiez toujours l'intégrité des fichiers déchiffrés

### Paramètres recommandés
- **Argon2**: memory_cost=65536, time_cost=3, parallelism=4
- **Mots de passe**: Minimum 12 caractères avec complexité élevée
- **Clés RSA**: 2048 bits minimum, 4096 bits recommandé

### Avertissements
- Les fichiers chiffrés contiennent des métadonnées (taille, nom original)
- L'application ne protège pas contre les keyloggers ou malware
- Utilisez toujours un environnement de confiance

## 📊 Tests de sécurité

### Analyse de force de mot de passe
```bash
python main.py password-strength --check
```

### Simulation d'attaque (module attacks/)
```bash
python attacks/bruteforce.py
```

### Validation de fichiers
```bash
python main.py analyze -f fichier.enc
```

## 🏗️ Architecture

```
Chiffrement/
├── core/                   # Modules principaux
│   ├── crypto_engine.py     # Moteur de chiffrement
│   ├── key_manager.py      # Gestion des clés
│   └── validators.py       # Validation des entrées
├── methods/                # Algorithmes de chiffrement
│   ├── aes_gcm_argon2.py   # AES-GCM avec Argon2
│   ├── aes_cbc_hmac.py     # AES-CBC avec HMAC
│   └── chacha20_poly1305.py # ChaCha20-Poly1305
├── ui/                     # Interface utilisateur
│   ├── cli.py              # Interface en ligne de commande
│   └── display.py          # Gestion de l'affichage
├── attacks/                # Tests de sécurité
│   └── bruteforce.py       # Simulation d'attaques
├── main.py                 # Point d'entrée
└── requirements.txt        # Dépendances
```

## 🔧 Développement

### Structure des classes
- `CryptoEngine`: Moteur principal de chiffrement
- `CryptoMethod`: Interface abstraite pour les algorithmes
- `KeyManager`: Gestion des clés et dérivation
- `DisplayManager`: Affichage formaté et couleurs
- `BruteForceAttack`: Tests de sécurité simulés

### Ajout d'une nouvelle méthode
1. Créer une classe héritant de `CryptoMethod`
2. Implémenter `encrypt()`, `decrypt()`, `get_method_name()`
3. Ajouter le register dans `crypto_engine.py`
4. Ajouter les tests appropriés

### Tests
```bash
# Test des modules individuels
python -m pytest tests/

# Test de l'interface CLI
python main.py --help
python main.py list-methods
```

## 📝 Exemples d'utilisation

### Scénario 1: Chiffrement de document sensible
```bash
# Chiffrement avec la méthode la plus sécurisée
python main.py encrypt -f rapport_confidentiel.pdf -m aes-gcm-argon2

# Analyse du fichier chiffré
python main.py analyze -f rapport_confidentiel.pdf.enc
```

### Scénario 2: Compatibility avec systèmes existants
```bash
# Chiffrement compatible
python main.py encrypt -f donnees.csv -m aes-cbc-hmac -o donnees.secure

# Déchiffrement sur autre système
python main.py decrypt -f donnees.secure -o donnees.csv
```

### Scénario 3: Test de sécurité
```bash
# Test de force du mot de passe
python main.py password-strength --check

# Analyse de la sécurité d'un fichier
python main.py analyze -f fichier_sensible.enc
```

## 🐛 Dépannage

### Problèmes courants

**ImportError: No module named 'cryptography'**
```bash
pip install cryptography
```

**Permission denied lors de la lecture/écriture**
```bash
# Vérifier les permissions du fichier
ls -la fichier.pdf
chmod 600 fichier_chiffre.enc
```

**Mot de passe incorrect**
- Vérifiez la casse (sensible à la casse)
- Confirmez qu'il n'y a pas d'espace supplémentaire
- Utilisez `password-strength` pour vérifier

### Fichiers de log
L'application affiche les erreurs directement dans la console. Pour déboguer, utilisez le mode verbeux si disponible.

## 📄 Licence

Ce projet est éducatif et destiné à l'apprentissage de la cryptographie. Utilisez-le de manière responsable et conformément aux lois en vigueur.

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez respecter les standards de codage et ajouter des tests appropriés.

## ⚠️ Avertissement

Cet outil est destiné à des fins éducatives et de test. Ne l'utilisez pas pour des données critiques sans une évaluation approfondie de la sécurité.
# Fortress
# Fortress
