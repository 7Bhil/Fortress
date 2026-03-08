import argparse
import getpass
import os
import sys
from typing import Optional
from pathlib import Path

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.crypto_engine import crypto_engine
from core.key_manager import key_manager
from ui.display import DisplayManager

class CryptoCLI:
    """Interface en ligne de commande pour l'application de chiffrement"""
    
    def __init__(self):
        self.display = DisplayManager()
        self.engine = crypto_engine
    
    def create_parser(self):
        """Crée le parser pour les arguments en ligne de commande"""
        parser = argparse.ArgumentParser(
            description="Outil de chiffrement/déchiffrement avancé",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation:
  %(prog)s encrypt -f document.pdf -m aes-gcm-argon2
  %(prog)s decrypt -f document.pdf.enc
  %(prog)s list-methods
  %(prog)s analyze -f document.pdf.enc
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
        
        # Commande encrypt
        encrypt_parser = subparsers.add_parser('encrypt', help='Chiffrer un fichier')
        encrypt_parser.add_argument('-f', '--file', required=True, help='Fichier à chiffrer')
        encrypt_parser.add_argument('-m', '--method', required=True, 
                                  choices=self.engine.get_available_methods(),
                                  help='Méthode de chiffrement')
        encrypt_parser.add_argument('-o', '--output', help='Fichier de sortie')
        encrypt_parser.add_argument('--memory-cost', type=int, default=65536,
                                  help='Coût mémoire Argon2 (défaut: 65536)')
        encrypt_parser.add_argument('--time-cost', type=int, default=3,
                                  help='Coût temps Argon2 (défaut: 3)')
        encrypt_parser.add_argument('--parallelism', type=int, default=4,
                                  help='Parallélisme Argon2 (défaut: 4)')
        
        # Commande decrypt
        decrypt_parser = subparsers.add_parser('decrypt', help='Déchiffrer un fichier')
        decrypt_parser.add_argument('-f', '--file', required=True, help='Fichier à déchiffrer')
        decrypt_parser.add_argument('-o', '--output', help='Fichier de sortie')
        
        # Commande list-methods
        list_parser = subparsers.add_parser('list-methods', help='Lister les méthodes disponibles')
        
        # Commande info
        info_parser = subparsers.add_parser('info', help='Informations sur une méthode')
        info_parser.add_argument('-m', '--method', required=True,
                                choices=self.engine.get_available_methods(),
                                help='Méthode à décrire')
        
        # Commande analyze
        analyze_parser = subparsers.add_parser('analyze', help='Analyser un fichier chiffré')
        analyze_parser.add_argument('-f', '--file', required=True, help='Fichier à analyser')
        
        # Commande password-strength
        password_parser = subparsers.add_parser('password-strength', help='Tester la force d\'un mot de passe')
        password_parser.add_argument('--check', action='store_true', 
                                   help='Vérifier la force d\'un mot de passe')
        
        # Commande generate-key
        keygen_parser = subparsers.add_parser('generate-key', help='Générer des clés')
        keygen_parser.add_argument('-t', '--type', choices=['aes', 'rsa'], default='aes',
                                  help='Type de clé à générer')
        keygen_parser.add_argument('-s', '--size', type=int, help='Taille de la clé')
        keygen_parser.add_argument('-o', '--output', help='Fichier de sortie pour la clé')
        
        return parser
    
    def get_password(self, confirm: bool = False) -> str:
        """Demande un mot de passe à l'utilisateur"""
        while True:
            password = getpass.getpass("Mot de passe: ")
            if not password:
                self.display.error("Le mot de passe ne peut pas être vide")
                continue
            
            if confirm:
                confirm_password = getpass.getpass("Confirmez le mot de passe: ")
                if password != confirm_password:
                    self.display.error("Les mots de passe ne correspondent pas")
                    continue
            
            # Vérification de la force du mot de passe
            strength = key_manager.validate_password_strength(password)
            if strength['score'] < 2:
                self.display.warning(f"Mot de passe {strength['strength'].lower()}")
                for feedback in strength['feedback']:
                    self.display.warning(f"  - {feedback}")
                
                response = input("Continuer quand même? (o/N): ").lower()
                if response != 'o':
                    continue
            else:
                self.display.success(f"Mot de passe {strength['strength'].lower()}")
            
            return password
    
    def cmd_encrypt(self, args):
        """Gère la commande d'encryption"""
        # Vérification du fichier
        if not os.path.exists(args.file):
            self.display.error(f"Le fichier {args.file} n'existe pas")
            return False
        
        # Demande du mot de passe
        self.display.info("Chiffrement du fichier...")
        password = self.get_password(confirm=True)
        
        # Paramètres pour le chiffrement
        kwargs = {
            'memory_cost': args.memory_cost,
            'time_cost': args.time_cost,
            'parallelism': args.parallelism
        }
        
        # Chiffrement
        result = self.engine.encrypt_file(
            file_path=args.file,
            password=password,
            method=args.method,
            output_path=args.output,
            **kwargs
        )
        
        if result.success:
            self.display.success(f"Fichier chiffré avec succès: {args.file}.enc")
            self.display.info(f"Méthode: {result.method}")
            self.display.info(f"Taille originale: {result.metadata.get('original_size', 'N/A')} octets")
            
            # Affichage des informations de sécurité
            if 'argon2_params' in result.metadata:
                params = result.metadata['argon2_params']
                self.display.info("Paramètres Argon2:")
                self.display.info(f"  - Coût mémoire: {params['memory_cost']}")
                self.display.info(f"  - Coût temps: {params['time_cost']}")
                self.display.info(f"  - Parallélisme: {params['parallelism']}")
            
            return True
        else:
            self.display.error(f"Échec du chiffrement: {result.error_message}")
            return False
    
    def cmd_decrypt(self, args):
        """Gère la commande de déchiffrement"""
        # Vérification du fichier
        if not os.path.exists(args.file):
            self.display.error(f"Le fichier {args.file} n'existe pas")
            return False
        
        # Demande du mot de passe
        self.display.info("Déchiffrement du fichier...")
        password = self.get_password()
        
        # Déchiffrement
        result = self.engine.decrypt_file(
            encrypted_file_path=args.file,
            password=password,
            output_path=args.output
        )
        
        if result.success:
            self.display.success(f"Fichier déchiffré avec succès")
            self.display.info(f"Méthode: {result.metadata.get('algorithm', 'N/A')}")
            self.display.info(f"Fichier original: {result.metadata.get('original_filename', 'N/A')}")
            self.display.info(f"Taille: {len(result.decrypted_data)} octets")
            
            # Vérification de l'intégrité
            if 'original_hash' in result.metadata:
                self.display.success("Intégrité vérifiée ✓")
            
            return True
        else:
            self.display.error(f"Échec du déchiffrement: {result.error_message}")
            return False
    
    def cmd_list_methods(self, args):
        """Liste les méthodes de chiffrement disponibles"""
        methods = self.engine.get_available_methods()
        
        self.display.header("Méthodes de chiffrement disponibles:")
        
        for method_name in methods:
            try:
                # Récupération des infos de la méthode
                method = self.engine.methods[method_name]
                if hasattr(method, 'get_info'):
                    info = method.get_info()
                    self.display.info(f"\n🔐 {info['display_name']} ({method_name})")
                    self.display.info(f"   {info['description']}")
                    self.display.info(f"   Sécurité: {info['security_level']}")
                    
                    # Cas d'usage recommandés
                    if 'recommended_use_cases' in info:
                        self.display.info("   Usage recommandé:")
                        for use_case in info['recommended_use_cases']:
                            self.display.info(f"     • {use_case}")
                else:
                    self.display.info(f"🔐 {method_name}")
            except Exception as e:
                self.display.warning(f"Erreur avec {method_name}: {str(e)}")
    
    def cmd_info(self, args):
        """Affiche des informations détaillées sur une méthode"""
        method_name = args.method
        
        if method_name not in self.engine.methods:
            self.display.error(f"Méthode {method_name} non trouvée")
            return False
        
        method = self.engine.methods[method_name]
        
        if hasattr(method, 'get_info'):
            info = method.get_info()
            self.display.header(f"Informations: {info['display_name']}")
            self.display.info(f"Nom interne: {info['name']}")
            self.display.info(f"Description: {info['description']}")
            self.display.info(f"Niveau de sécurité: {info['security_level']}")
            
            self.display.info("\nCaractéristiques:")
            for feature in info['features']:
                self.display.info(f"  ✓ {feature}")
            
            self.display.info("\nCas d'usage recommandés:")
            for use_case in info['recommended_use_cases']:
                self.display.info(f"  • {use_case}")
        else:
            self.display.info(f"Méthode: {method_name}")
            self.display.info("Aucune information détaillée disponible")
        
        return True
    
    def cmd_analyze(self, args):
        """Analyse un fichier chiffré"""
        if not os.path.exists(args.file):
            self.display.error(f"Le fichier {args.file} n'existe pas")
            return False
        
        try:
            # Lecture des métadonnées du fichier
            encrypted_data, metadata, method = self.engine._load_encrypted_file(args.file)
            
            self.display.header(f"Analyse du fichier: {args.file}")
            self.display.info(f"Méthode de chiffrement: {method}")
            self.display.info(f"Algorithme: {metadata.get('algorithm', 'N/A')}")
            
            if 'original_filename' in metadata:
                self.display.info(f"Fichier original: {metadata['original_filename']}")
            
            if 'original_size' in metadata:
                size = metadata['original_size']
                self.display.info(f"Taille originale: {size} octets ({self._format_size(size)})")
            
            if 'argon2_params' in metadata:
                params = metadata['argon2_params']
                self.display.info("\nParamètres Argon2:")
                self.display.info(f"  - Coût mémoire: {params['memory_cost']:,}")
                self.display.info(f"  - Coût temps: {params['time_cost']} itérations")
                self.display.info(f"  - Parallélisme: {params['parallelism']}")
                self.display.info(f"  - Longueur de sel: {params['salt_length']} octets")
            
            if 'pbkdf2_params' in metadata:
                params = metadata['pbkdf2_params']
                self.display.info("\nParamètres PBKDF2:")
                self.display.info(f"  - Itérations: {params['iterations']:,}")
                self.display.info(f"  - Longueur de sel: {params['salt_length']} octets")
                self.display.info(f"  - Longueur de clé: {params['key_length']} octets")
            
            # Taille des données chiffrées
            self.display.info(f"\nTaille chiffrée: {len(encrypted_data)} octets ({self._format_size(len(encrypted_data))})")
            
            # Évaluation de la sécurité
            self.display.info("\nÉvaluation de sécurité:")
            if method in ['aes-gcm-argon2', 'chacha20-poly1305']:
                self.display.success("  ✓ Sécurité très élevée")
            elif method == 'aes-cbc-hmac':
                self.display.success("  ✓ Sécurité élevée")
            else:
                self.display.warning("  ⚠ Sécurité inconnue")
            
            return True
            
        except Exception as e:
            self.display.error(f"Erreur lors de l'analyse: {str(e)}")
            return False
    
    def cmd_password_strength(self, args):
        """Teste la force d'un mot de passe"""
        if args.check:
            password = getpass.getpass("Entrez le mot de passe à tester: ")
        else:
            password = getpass.getpass("Nouveau mot de passe: ")
        
        strength = key_manager.validate_password_strength(password)
        
        self.display.header("Analyse de la force du mot de passe")
        self.display.info(f"Longueur: {strength['length']} caractères")
        self.display.info(f"Score: {strength['score']}/6")
        
        # Affichage du niveau avec couleur
        if strength['strength'] == 'Très fort':
            self.display.success(f"Niveau: {strength['strength']}")
        elif strength['strength'] == 'Fort':
            self.display.success(f"Niveau: {strength['strength']}")
        elif strength['strength'] == 'Moyen':
            self.display.warning(f"Niveau: {strength['strength']}")
        else:
            self.display.error(f"Niveau: {strength['strength']}")
        
        if strength['feedback']:
            self.display.info("\nRecommandations:")
            for feedback in strength['feedback']:
                self.display.info(f"  • {feedback}")
    
    def cmd_generate_key(self, args):
        """Génère des clés cryptographiques"""
        if args.type == 'aes':
            key_size = args.size or 32
            key = key_manager.generate_aes_key(key_size)
            
            self.display.header(f"Génération de clé AES-{key_size * 8}")
            self.display.info(f"Clé générée ({key_size} octets):")
            self.display.code(key.hex())
            
            if args.output:
                with open(args.output, 'wb') as f:
                    f.write(key)
                self.display.success(f"Clé sauvegardée dans: {args.output}")
        
        elif args.type == 'rsa':
            key_size = args.size or 2048
            keypair = key_manager.generate_rsa_keypair(key_size)
            
            if keypair.success:
                self.display.header(f"Génération de paire de clés RSA-{key_size}")
                
                if args.output:
                    # Sauvegarde de la clé privée
                    private_key_path = f"{args.output}.private.pem"
                    with open(private_key_path, 'wb') as f:
                        f.write(keypair.private_key)
                    
                    # Sauvegarde de la clé publique
                    public_key_path = f"{args.output}.public.pem"
                    with open(public_key_path, 'wb') as f:
                        f.write(keypair.public_key)
                    
                    self.display.success(f"Clé privée: {private_key_path}")
                    self.display.success(f"Clé publique: {public_key_path}")
                else:
                    self.display.info("Clé privée:")
                    self.display.code(keypair.private_key.decode('utf-8'))
                    self.display.info("Clé publique:")
                    self.display.code(keypair.public_key.decode('utf-8'))
            else:
                self.display.error(f"Erreur de génération RSA: {keypair.error_message}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Formate une taille en octets pour l'affichage"""
        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} To"
    
    def run(self, args=None):
        """Point d'entrée principal de la CLI"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return False
        
        try:
            # Exécution de la commande appropriée
            if parsed_args.command == 'encrypt':
                return self.cmd_encrypt(parsed_args)
            elif parsed_args.command == 'decrypt':
                return self.cmd_decrypt(parsed_args)
            elif parsed_args.command == 'list-methods':
                return self.cmd_list_methods(parsed_args)
            elif parsed_args.command == 'info':
                return self.cmd_info(parsed_args)
            elif parsed_args.command == 'analyze':
                return self.cmd_analyze(parsed_args)
            elif parsed_args.command == 'password-strength':
                return self.cmd_password_strength(parsed_args)
            elif parsed_args.command == 'generate-key':
                return self.cmd_generate_key(parsed_args)
            else:
                self.display.error(f"Commande inconnue: {parsed_args.command}")
                return False
                
        except KeyboardInterrupt:
            self.display.warning("\nOpération annulée par l'utilisateur")
            return False
        except Exception as e:
            self.display.error(f"Erreur inattendue: {str(e)}")
            return False

def main():
    """Point d'entrée pour la CLI"""
    cli = CryptoCLI()
    success = cli.run()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()