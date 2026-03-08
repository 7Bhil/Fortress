import os
import secrets
import hashlib
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend  # Plus nécessaire
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hmac

@dataclass
class KeyDerivationResult:
    """Résultat de la dérivation de clé"""
    key: bytes
    salt: bytes
    parameters: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

@dataclass
class KeyPair:
    """Paire de clés asymétriques"""
    private_key: bytes
    public_key: bytes
    success: bool
    error_message: Optional[str] = None

class KeyManager:
    """Gestionnaire de clés cryptographiques"""
    
    def __init__(self):
        # self.backend = default_backend()  # Plus nécessaire dans les nouvelles versions
        pass
    
    def derive_key_argon2(self, password: str, salt: Optional[bytes] = None, 
                         key_length: int = 32, memory_cost: int = 65536,
                         time_cost: int = 3, parallelism: int = 4) -> KeyDerivationResult:
        """
        Dérive une clé à partir d'un mot de passe avec Argon2id
        
        Args:
            password: Mot de passe à dériver
            salt: Sel optionnel (généré si non fourni)
            key_length: Longueur de la clé en octets
            memory_cost: Coût mémoire pour Argon2
            time_cost: Nombre d'itérations
            parallelism: Parallélisme
        
        Returns:
            KeyDerivationResult: Clé dérivée et métadonnées
        """
        try:
            if salt is None:
                salt = secrets.token_bytes(16)
            
            # Conversion du mot de passe en bytes
            password_bytes = password.encode('utf-8')
            
            # Configuration Argon2id
            kdf = Argon2id(
                salt=salt,
                length=key_length,
                memory_cost=memory_cost,
                iterations=time_cost,  # Changé de time_cost à iterations
                lanes=parallelism      # Changé de parallelism à lanes
                # backend=self.backend  # Supprimé - plus nécessaire
            )
            
            # Dérivation de la clé
            key = kdf.derive(password_bytes)
            
            parameters = {
                'algorithm': 'Argon2id',
                'key_length': key_length,
                'memory_cost': memory_cost,
                'time_cost': time_cost,
                'parallelism': parallelism,
                'salt_length': len(salt)
            }
            
            return KeyDerivationResult(
                key=key,
                salt=salt,
                parameters=parameters,
                success=True
            )
            
        except Exception as e:
            return KeyDerivationResult(
                key=b'',
                salt=b'',
                parameters={},
                success=False,
                error_message=f"Erreur de dérivation Argon2: {str(e)}"
            )
    
    def derive_key_pbkdf2(self, password: str, salt: Optional[bytes] = None,
                         key_length: int = 32, iterations: int = 100000) -> KeyDerivationResult:
        """
        Dérive une clé à partir d'un mot de passe avec PBKDF2
        
        Args:
            password: Mot de passe à dériver
            salt: Sel optionnel (généré si non fourni)
            key_length: Longueur de la clé en octets
            iterations: Nombre d'itérations
        
        Returns:
            KeyDerivationResult: Clé dérivée et métadonnées
        """
        try:
            if salt is None:
                salt = secrets.token_bytes(16)
            
            password_bytes = password.encode('utf-8')
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=key_length,
                salt=salt,
                iterations=iterations
            )
            
            key = kdf.derive(password_bytes)
            
            parameters = {
                'algorithm': 'PBKDF2-HMAC-SHA256',
                'key_length': key_length,
                'iterations': iterations,
                'salt_length': len(salt)
            }
            
            return KeyDerivationResult(
                key=key,
                salt=salt,
                parameters=parameters,
                success=True
            )
            
        except Exception as e:
            return KeyDerivationResult(
                key=b'',
                salt=b'',
                parameters={},
                success=False,
                error_message=f"Erreur de dérivation PBKDF2: {str(e)}"
            )
    
    def generate_aes_key(self, key_length: int = 32) -> bytes:
        """
        Génère une clé AES aléatoire
        
        Args:
            key_length: Longueur de la clé (16 pour AES-128, 24 pour AES-192, 32 pour AES-256)
        
        Returns:
            bytes: Clé AES générée
        """
        return secrets.token_bytes(key_length)
    
    def generate_rsa_keypair(self, key_size: int = 2048) -> KeyPair:
        """
        Génère une paire de clés RSA
        
        Args:
            key_size: Taille de la clé RSA (1024, 2048, 4096)
        
        Returns:
            KeyPair: Paire de clés RSA sérialisées
        """
        try:
            # Génération de la clé privée RSA
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
                # backend=self.backend  # Supprimé
            )
            
            # Sérialisation de la clé privée
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Sérialisation de la clé publique
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            return KeyPair(
                private_key=private_pem,
                public_key=public_pem,
                success=True
            )
            
        except Exception as e:
            return KeyPair(
                private_key=b'',
                public_key=b'',
                success=False,
                error_message=f"Erreur de génération RSA: {str(e)}"
            )
    
    def generate_random_iv(self, length: int = 16) -> bytes:
        """
        Génère un IV (vecteur d'initialisation) aléatoire
        
        Args:
            length: Longueur de l'IV en octets
        
        Returns:
            bytes: IV généré
        """
        return secrets.token_bytes(length)
    
    def generate_random_nonce(self, length: int = 12) -> bytes:
        """
        Génère un nonce aléatoire pour les algorithmes comme AES-GCM
        
        Args:
            length: Longueur du nonce en octets
        
        Returns:
            bytes: Nonce généré
        """
        return secrets.token_bytes(length)
    
    def derive_hmac_key(self, key: bytes, purpose: str = "HMAC") -> bytes:
        """
        Dérive une clé HMAC à partir d'une clé principale
        
        Args:
            key: Clé principale
            purpose: Usage de la clé HMAC
        
        Returns:
            bytes: Clé HMAC dérivée
        """
        return hashlib.sha256(key + purpose.encode('utf-8')).digest()
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Évalue la force d'un mot de passe
        
        Args:
            password: Mot de passe à évaluer
        
        Returns:
            Dict: Résultats de l'évaluation
        """
        score = 0
        feedback = []
        
        # Longueur
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Le mot de passe doit contenir au moins 8 caractères")
        
        # Complexité
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if has_upper:
            score += 1
        else:
            feedback.append("Ajoutez des majuscules")
        
        if has_lower:
            score += 1
        else:
            feedback.append("Ajoutez des minuscules")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Ajoutez des chiffres")
        
        if has_special:
            score += 1
        else:
            feedback.append("Ajoutez des caractères spéciaux")
        
        # Évaluation finale
        if score >= 6:
            strength = "Très fort"
        elif score >= 4:
            strength = "Fort"
        elif score >= 2:
            strength = "Moyen"
        else:
            strength = "Faible"
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'length': len(password)
        }
    
    def secure_erase(self, data: bytearray):
        """
        Efface sécuritairement des données sensibles en mémoire
        
        Args:
            data: Données à effacer
        """
        for i in range(len(data)):
            data[i] = 0
    
    def generate_key_from_entropy(self, entropy_source: str, key_length: int = 32) -> bytes:
        """
        Génère une clé à partir d'une source d'entropie
        
        Args:
            entropy_source: Source d'entropie (phrase, etc.)
            key_length: Longueur de la clé souhaitée
        
        Returns:
            bytes: Clé générée
        """
        return hashlib.sha256(entropy_source.encode('utf-8')).digest()[:key_length]

# Instance globale du gestionnaire de clés
key_manager = KeyManager()