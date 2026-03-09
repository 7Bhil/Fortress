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
from core.crypto_engine import crypto_engine
from ui.display import DisplayManager

def interactive_mode():
    """Mode interactif avec menu guidé"""
    display = DisplayManager()
    
    # Message d'accueil avec signature
    display.header("🏰 BIENVENUE DANS FORTRESS")
    print("✨ Framework cryptographique créé par Bhilal CHITOU (Bhil€)")
    print("🔐 Protégez vos données avec des algorithmes de niveau militaire")
    print("📧 Contact : 7bhilal.chitou7@gmail.com")
    print("")
    
    while True:
        display.header("🏰 FORTRESS - Menu Principal")
        print("1. 🔐 Chiffrer")
        print("2. 🔓 Déchiffrer")
        print("3. 📋 Lister les méthodes")
        print("4. ℹ️ Informations sur une méthode")
        print("5. 🔍 Analyser un fichier")
        print("6. 🔑 Générer des clés")
        print("7. 💪 Tester la force d'un mot de passe")
        print("8. ❌ Quitter")
        
        try:
            choice = input("\nVotre choix (1-8): ").strip()
            
            if choice == "1":
                encrypt_menu(display)
            elif choice == "2":
                decrypt_menu(display)
            elif choice == "3":
                list_methods_menu(display)
            elif choice == "4":
                info_menu(display)
            elif choice == "5":
                analyze_menu(display)
            elif choice == "6":
                generate_key_menu(display)
            elif choice == "7":
                password_strength_menu(display)
            elif choice == "8":
                display.success("✓ Au revoir !")
                print("🙏 Merci d'avoir utilisé Fortress - Bhilal CHITOU (Bhil€)")
                print("📧 Pour me contacter : 7bhilal.chitou7@gmail.com")
                break
            else:
                display.error("Choix invalide. Réessayez.")
                
        except KeyboardInterrupt:
            display.warning("\nOpération annulée. Retour au menu principal.")
        except Exception as e:
            display.error(f"Erreur: {str(e)}")

def encrypt_menu(display):
    """Menu de chiffrement"""
    display.header("🔐 MENU CHIFFREMENT")
    print("1. Chiffrer un message")
    print("2. Chiffrer un fichier")
    print("3. Choisir la méthode de chiffrement")
    print("4. Retour au menu principal")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    if choice == "1":
        encrypt_message(display)
    elif choice == "2":
        encrypt_file_menu(display)
    elif choice == "3":
        choose_method_menu(display)
    elif choice == "4":
        return
    else:
        display.error("Choix invalide.")

def decrypt_menu(display):
    """Menu de déchiffrement"""
    display.header("🔓 MENU DÉCHIFFREMENT")
    print("1. Déchiffrer un message")
    print("2. Déchiffrer un fichier")
    print("3. Retour au menu principal")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        decrypt_message(display)
    elif choice == "2":
        decrypt_file_menu(display)
    elif choice == "3":
        return
    else:
        display.error("Choix invalide.")

def encrypt_message(display):
    """Chiffrer un message texte"""
    display.info("Chiffrement d'un message")
    
    message = input("Entrez votre message: ")
    if not message:
        display.error("Le message ne peut pas être vide.")
        return
    
    # Choix de la méthode
    methods = crypto_engine.get_available_methods()
    display.info("\nMéthodes disponibles:")
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method}")
    
    try:
        method_choice = int(input(f"Choisissez une méthode (1-{len(methods)}): ")) - 1
        if 0 <= method_choice < len(methods):
            method = methods[method_choice]
        else:
            display.error("Choix invalide.")
            return
    except ValueError:
        display.error("Entrez un nombre valide.")
        return
    
    import getpass
    password = getpass.getpass("Mot de passe: ")
    confirm = getpass.getpass("Confirmez le mot de passe: ")
    
    if password != confirm:
        display.error("Les mots de passe ne correspondent pas.")
        return
    
    # Chiffrement
    try:
        result = crypto_engine.encrypt_data(message.encode('utf-8'), password, method)
        if result.success:
            display.success("Message chiffré avec succès !")
            display.info("Message chiffré (copiez-le):")
            display.code(result.encrypted_data.decode('utf-8'))
        else:
            display.error(f"Erreur: {result.error_message}")
    except Exception as e:
        display.error(f"Erreur de chiffrement: {str(e)}")

def decrypt_message(display):
    """Déchiffrer un message texte"""
    display.info("Déchiffrement d'un message")
    
    message = input("Entrez le message chiffré: ")
    if not message:
        display.error("Le message ne peut pas être vide.")
        return
    
    import getpass
    password = getpass.getpass("Mot de passe: ")
    
    try:
        # Utiliser la nouvelle fonction decrypt_message
        result = crypto_engine.decrypt_message(message, password)
        if result.success:
            display.success("Message déchiffré avec succès !")
            display.info("Message original:")
            
            # Essayer de décoder en UTF-8, sinon afficher en hexadécimal
            try:
                decoded_text = result.decrypted_data.decode('utf-8')
                display.code(decoded_text)
            except UnicodeDecodeError:
                display.info("Données binaires (affichage en hexadécimal):")
                display.code(result.decrypted_data.hex())
            
            display.info(f"Méthode utilisée: {result.metadata.get('method', 'Inconnue')}")
        else:
            display.error(f"Erreur: {result.error_message}")
    except Exception as e:
        display.error(f"Erreur de déchiffrement: {str(e)}")

def encrypt_file_menu(display):
    """Chiffrer un fichier"""
    file_path = input("Chemin du fichier à chiffrer: ")
    if not os.path.exists(file_path):
        display.error("Le fichier n'existe pas.")
        return
    
    methods = crypto_engine.get_available_methods()
    display.info("\nMéthodes disponibles:")
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method}")
    
    try:
        method_choice = int(input(f"Choisissez une méthode (1-{len(methods)}: ")) - 1
        if 0 <= method_choice < len(methods):
            method = methods[method_choice]
        else:
            display.error("Choix invalide.")
            return
    except ValueError:
        display.error("Entrez un nombre valide.")
        return
    
    import getpass
    password = getpass.getpass("Mot de passe: ")
    confirm = getpass.getpass("Confirmez le mot de passe: ")
    
    if password != confirm:
        display.error("Les mots de passe ne correspondent pas.")
        return
    
    try:
        result = crypto_engine.encrypt_file(file_path, password, method)
        if result.success:
            display.success(f"Fichier chiffré: {file_path}.enc")
            display.info(f"Méthode: {method}")
            display.info(f"Taille: {result.metadata.get('original_size', 'N/A')} octets")
        else:
            display.error(f"Erreur: {result.error_message}")
    except Exception as e:
        display.error(f"Erreur: {str(e)}")

def decrypt_file_menu(display):
    """Déchiffrer un fichier"""
    file_path = input("Chemin du fichier à déchiffrer: ")
    if not os.path.exists(file_path):
        display.error("Le fichier n'existe pas.")
        return
    
    import getpass
    password = getpass.getpass("Mot de passe: ")
    
    try:
        result = crypto_engine.decrypt_file(file_path, password)
        if result.success:
            display.success("Fichier déchiffré avec succès !")
            display.info(f"Fichier original: {result.metadata.get('original_filename', 'N/A')}")
            display.info(f"Taille: {len(result.decrypted_data)} octets")
        else:
            display.error(f"Erreur: {result.error_message}")
    except Exception as e:
        display.error(f"Erreur: {str(e)}")

def list_methods_menu(display):
    """Lister les méthodes disponibles"""
    methods = crypto_engine.get_available_methods()
    
    display.header("🔐 MÉTHODES DE CHIFFREMENT")
    for i, method_name in enumerate(methods, 1):
        try:
            method = crypto_engine.methods[method_name]
            if hasattr(method, 'get_info'):
                info = method.get_info()
                print(f"\n{i}. 🔐 {info['display_name']}")
                print(f"   {info['description']}")
                print(f"   Sécurité: {info['security_level']}")
        except:
            print(f"{i}. 🔐 {method_name}")

def info_menu(display):
    """Informations sur une méthode"""
    methods = crypto_engine.get_available_methods()
    
    print("\nMéthodes disponibles:")
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method}")
    
    try:
        choice = int(input(f"Choisissez une méthode (1-{len(methods)}): ")) - 1
        if 0 <= choice < len(methods):
            method_name = methods[choice]
            method = crypto_engine.methods[method_name]
            
            if hasattr(method, 'get_info'):
                info = method.get_info()
                display.header(f"ℹ️ {info['display_name']}")
                display.info(f"Description: {info['description']}")
                display.info(f"Sécurité: {info['security_level']}")
                
                print("\nCaractéristiques:")
                for feature in info['features']:
                    print(f"  ✓ {feature}")
            else:
                display.info(f"Méthode: {method_name}")
        else:
            display.error("Choix invalide.")
    except ValueError:
        display.error("Entrez un nombre valide.")

def analyze_menu(display):
    """Analyser un fichier chiffré"""
    file_path = input("Chemin du fichier à analyser: ")
    
    if not os.path.exists(file_path):
        display.error("Le fichier n'existe pas.")
        return
    
    try:
        encrypted_data, metadata, method = crypto_engine._load_encrypted_file(file_path)
        
        display.header(f"🔍 ANALYSE DU FICHIER")
        display.info(f"Méthode: {method}")
        display.info(f"Algorithme: {metadata.get('algorithm', 'N/A')}")
        
        if 'original_filename' in metadata:
            display.info(f"Fichier original: {metadata['original_filename']}")
        
        if 'original_size' in metadata:
            size = metadata['original_size']
            display.info(f"Taille originale: {size} octets")
        
        display.info(f"Taille chiffrée: {len(encrypted_data)} octets")
        
    except Exception as e:
        display.error(f"Erreur d'analyse: {str(e)}")

def generate_key_menu(display):
    """Générer des clés"""
    display.header("🔑 GÉNÉRATION DE CLÉS")
    print("1. Clé AES")
    print("2. Paire de clés RSA")
    print("3. Retour")
    
    choice = input("Votre choix (1-3): ").strip()
    
    if choice == "1":
        try:
            from core.key_manager import key_manager
            key = key_manager.generate_aes_key(32)
            display.success("Clé AES-256 générée:")
            display.code(key.hex())
        except Exception as e:
            display.error(f"Erreur: {str(e)}")
    
    elif choice == "2":
        try:
            from core.key_manager import key_manager
            keypair = key_manager.generate_rsa_keypair(2048)
            if keypair.success:
                display.success("Paire de clés RSA-2048 générée:")
                display.info("Clé privée:")
                display.code(keypair.private_key.decode('utf-8')[:100] + "...")
                display.info("Clé publique:")
                display.code(keypair.public_key.decode('utf-8')[:100] + "...")
            else:
                display.error(f"Erreur: {keypair.error_message}")
        except Exception as e:
            display.error(f"Erreur: {str(e)}")

def password_strength_menu(display):
    """Tester la force d'un mot de passe"""
    display.header("💪 TEST DE FORCE DE MOT DE PASSE")
    
    import getpass
    password = getpass.getpass("Entrez le mot de passe à tester: ")
    
    try:
        from core.key_manager import key_manager
        strength = key_manager.validate_password_strength(password)
        
        display.info(f"Longueur: {strength['length']} caractères")
        display.info(f"Score: {strength['score']}/6")
        
        if strength['strength'] == 'Très fort':
            display.success(f"Niveau: {strength['strength']}")
        elif strength['strength'] == 'Fort':
            display.success(f"Niveau: {strength['strength']}")
        elif strength['strength'] == 'Moyen':
            display.warning(f"Niveau: {strength['strength']}")
        else:
            display.error(f"Niveau: {strength['strength']}")
        
        if strength['feedback']:
            display.info("\nRecommandations:")
            for feedback in strength['feedback']:
                display.info(f"  • {feedback}")
                
    except Exception as e:
        display.error(f"Erreur: {str(e)}")

def choose_method_menu(display):
    """Choisir une méthode de chiffrement"""
    methods = crypto_engine.get_available_methods()
    
    display.header("🔐 CHOIX DE LA MÉTHODE")
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method}")
    
    try:
        choice = int(input(f"Choisissez une méthode (1-{len(methods)}: ")) - 1
        if 0 <= choice < len(methods):
            selected_method = methods[choice]
            display.success(f"Méthode sélectionnée: {selected_method}")
            return selected_method
        else:
            display.error("Choix invalide.")
            return None
    except ValueError:
        display.error("Entrez un nombre valide.")
        return None

def show_banner():
    """Affiche la bannière de l'application"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🔐 Fortress v1.0.0 - Par Bhilal CHITOU (Bhil€)           ║
║                                                              ║
║    Framework cryptographique moderne avec :                  ║
║    • AES-GCM avec Argon2                                    ║
║    • AES-CBC avec HMAC                                      ║
║    • ChaCha20-Poly1305                                      ║
║    • Analyse de sécurité                                    ║
║                                                              ║
║    Created by Bhil€ (Bhilal CHITOU) - 2024                   ║
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
    # Vérification des dépendances
    if not check_dependencies():
        print("\n❌ Dépendances manquantes. Installation requise.")
        return 1
    
    # Mode interactif par défaut
    if len(sys.argv) == 1:
        show_banner()
        print("\n🏰 BIENVENUE DANS FORTRESS - Mode Interactif")
        print("Choisissez une option dans le menu ci-dessous:\n")
        interactive_mode()
        return 0
    
    # Mode CLI avec arguments
    try:
        return cli_main()
    except KeyboardInterrupt:
        print("\n\n⚠ Opération annulée par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur critique: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())