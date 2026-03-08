#!/usr/bin/env python3
"""
Outil de Chiffrement Avancé
Application complète de chiffrement/déchiffrement avec interface en ligne de commande

Auteur: BHIL
Version: 1.0.0
Description: Framework cryptographique moderne avec support de multiples algorithmes
"""

import sys
import os

# Ajout du répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.cli import main as cli_main

def show_banner():
    """Affiche la bannière de l'application"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🔐 Outil de Chiffrement Avancé v1.0.0                     ║
║                                                              ║
║    Framework cryptographique moderne avec :                  ║
║    • AES-GCM avec Argon2                                    ║
║    • AES-CBC avec HMAC                                      ║
║    • ChaCha20-Poly1305                                      ║
║    • Analyse de sécurité                                    ║
║                                                              ║
║    Usage: python main.py --help                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_dependencies():
    """Vérifie les dépendances requises"""
    try:
        import cryptography
        print("✓ Bibliothèque cryptography trouvée")
    except ImportError:
        print("✗ Bibliothèque cryptography manquante")
        print("  Installation: pip install cryptography")
        return False
    
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
        print("✓ Algorithmes AEAD disponibles")
    except ImportError:
        print("✗ Algorithmes AEAD non disponibles")
        return False
    
    return True

def main():
    """Point d'entrée principal de l'application"""
    # Affichage de la bannière seulement si pas d'arguments
    if len(sys.argv) == 1:
        show_banner()
        print("\nUtilisez --help pour voir les commandes disponibles\n")
        return 0
    
    # Vérification des dépendances
    if not check_dependencies():
        print("\n❌ Dépendances manquantes. Installation requise.")
        return 1
    
    try:
        # Lancement de la CLI
        return cli_main()
    except KeyboardInterrupt:
        print("\n\n⚠ Opération annulée par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur critique: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())