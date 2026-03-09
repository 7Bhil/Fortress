# 🏰 Fortress - Framework Cryptographique Universel

**Créé par Bhilal CHITOU (Bhil€) - 2024**

Outil de chiffrement accessible à tous - Protégez vos données en 3 clics !

---

## 👨‍💻 À propos du créateur

**Bhilal CHITOU (Bhil€)** est un développeur passionné par la cybersécurité et l'accessibilité technologique. Fortress est son projet phare visant à démocratiser la cryptographie pour tous.

**Contact :**
- 📧 7bhilal.chitou7@gmail.com
- 💼 LinkedIn : [votre-profil]
- 🐙 GitHub : https://github.com/7Bhil

---

## 🎯 Démarrage Rapide (Pour les Nuls)

### Étape 1 : Installation
```bash
# Clonez ou téléchargez le projet
cd votre-dossier/Fortress

# Installez les dépendances
pip install -r requirements.txt
```

### Étape 2 : Premier test
```bash
# Lancez Fortress
python main.py
```

### Étape 3 : Chiffrez votre premier fichier
1. Choisissez `1` (Chiffrer)
2. Choisissez `2` (Chiffrer un fichier)
3. Entrez le nom de votre fichier
4. Choisissez `1` (AES-GCM)
5. Entrez un mot de passe

**🎉 Félicitations ! Votre fichier est maintenant sécurisé !**

---

## 🚀 Fonctionnalités Principales

### 🔐 Chiffrement
- **TOUS les formats supportés** : PDF, MP4, MP3, ZIP, images...
- **3 algorithmes militaires** : AES-GCM, AES-CBC, ChaCha20
- **Interface simplifiée** : Plus besoin de commandes complexes

### 🔓 Déchiffrement
- **Détection automatique** de la méthode utilisée
- **Restauration parfaite** des fichiers originaux
- **Vérification d'intégrité** anti-corruption

### 🛡️ Sécurité
- **Testeur de mots de passe** : Évaluez vos passwords
- **Analyse de vulnérabilité** : Simulations d'attaques
- **Génération de clés** : Créez des clés RSA/AES

---

## 🎮 Mode Interactif (Le plus simple !)

**Lancez simplement :**
```bash
python main.py
```

**Le menu vous guide pas à pas :**

```
🏰 FORTRESS - Menu Principal
1. 🔐 Chiffrer
2. 🔓 Déchiffrer  
3. 📋 Lister les méthodes
4. ℹ️ Informations
5. 🔍 Analyser un fichier
6. 🔑 Générer des clés
7. 💪 Tester mot de passe
8. ❌ Quitter
```

**Plus besoin de mémoriser des commandes !**

---

## 📁 Cas d'Usage Réels

### 👨‍🎓 Étudiant
```bash
# Protéger vos cours
python main.py
# 1 → 2 → cours_math.pdf → 1 → "motdepassefort"
```

### 👨‍💼 Professionnel  
```bash
# Sécuriser documents sensibles
python main.py
# 1 → 2 → rapport_confidentiel.docx → 1 → "password2024"
```

### 🎵 Amateur
```bash
# Protéger votre musique
python main.py
# 1 → 2 → playlist_personnelle.mp3 → 1 → "musik123"
```

### 🎬 Vidéos
```bash
# Cacher vos films
python main.py
# 1 → 2 → film_prive.mp4 → 1 → "cinema2024"
```

---

## 🔧 Algorithmes Disponibles

### 1. 🛡️ AES-GCM avec Argon2 (Recommandé)
- **Niveau** : Militaire
- **Usage** : Documents sensibles, fichiers professionnels
- **Avantages** : Le plus sécurisé, authentification intégrée

### 2. 🔒 AES-CBC avec HMAC
- **Niveau** : Standard industriel
- **Usage** : Fichiers quotidiens, compatibilité maximale
- **Avantages** : Compatible avec tous les systèmes

### 3. ⚡ ChaCha20-Poly1305
- **Niveau** : Moderne ultra-rapide
- **Usage** : Mobile, streaming, gros fichiers
- **Avantages** : Le plus rapide, idéal pour les vidéos

---

## 📋 FAQ - Questions Courantes

**Q : J'ai une erreur "cryptography not found"**
R : Contactez-moi à 7bhilal.chitou7@gmail.com ou lancez `pip install -r requirements.txt`

**Q : Comment choisir entre AES-GCM et ChaCha20 ?**
R : AES-GCM pour desktop, ChaCha20 pour mobile/serveur

**Q : Puis-je chiffrer des images ?**
R : Oui ! Fortress fonctionne avec TOUS les types de fichiers

**Q : Mes fichiers sont-ils vraiment sécurisés ?**
R : Oui ! Utilise les mêmes algorithmes que la NSA et les banques

**Q : Comment déchiffrer ?**
R : `python main.py` → 2 → 2 → fichier.enc → même mot de passe

**Q : Puis-je partager les fichiers chiffrés ?**
R : Oui ! Seul le mot de passe permet de les lire

---

## 🎯 Exemples Pratiques

### Chiffrer un message secret
```bash
python main.py
# 1 → 1 → "message secret" → 1 → "password123"
# Résultat : {"encrypted_data": "...", "metadata": {...}}
```

### Déchiffrer un fichier
```bash
python main.py
# 2 → 2 → document.pdf.enc → même mot de passe
# Résultat : document.pdf restauré parfaitement
```

### Tester la force d'un mot de passe
```bash
python main.py
# 7 → "MonPassword123"
# Résultat : Score 8/10 - Très fort ✅
```

---

## 🛠️ Installation Avancée

### Environnement virtuel (Recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Vérification
```bash
python main.py --help
# Devrait afficher toutes les commandes disponibles
```

---

## 🔐 Sécurité et Fiabilité

### ✅ Garanties
- **Zéro connaissance** : Votre mot de passe n'est jamais stocké
- **Intégrité** : Détection automatique de corruption
- **Authentification** : Protection contre les modifications
- **Standard militaire** : Algorithmes validés par la NSA

### 🛡️ Menaces protégées
- **Force brute** : Tests de résistance intégrés
- **Dictionnaire** : Protection mots de passe faibles
- **Écoute** : Chiffrement de bout en bout
- **Corruption** : Vérification SHA-256 automatique

---

## 📞 Support et Contribuons

### 🐛 Bug trouvé ?
1. Contactez-moi directement : 7bhilal.chitou7@gmail.com
2. Notez l'erreur exacte
3. Donnez le fichier utilisé
4. Précisez votre système

### 🚀 Idées d'amélioration
- Interface graphique
- Chiffrement dans le cloud
- Gestion de mots de passe
- Plugin navigateur

---

## 📜 Licence

**Fortress** - Framework cryptographique éducatif et personnel

**Usage** : Libre pour usage personnel et éducatif  
**Commercial** : Contactez-nous pour licence entreprise

---

## 🎉 Conclusion

**Fortress rend la cryptographie accessible à tous :**

- ✅ **Simple** : Plus besoin d'être expert
- ✅ **Universel** : TOUS les fichiers supportés  
- ✅ **Sécurisé** : Niveau militaire
- ✅ ** Gratuit** : Open source et libre
- ✅ **Créé avec ❤️** par Bhilal CHITOU (Bhil€)

**Protégez vos données dès maintenant !**

```bash
git clone https://github.com/bhileu/Fortress
cd Fortress
python main.py
```

**Vos données méritent Fortress !** 🏰🔐

---

**© 2024 Bhilal CHITOU (Bhil€) - Tous droits réservés**
**Made with passion for cybersecurity and accessibility**
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
