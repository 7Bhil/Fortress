import os
import json
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from core.crypto_engine import CryptoMethod, EncryptionResult, DecryptionResult
from core.key_manager import key_manager

class AESGCMArgon2Method(CryptoMethod):
    """Implémentation du chiffrement AES-GCM avec dérivation de clé Argon2"""
    
    def __init__(self):
        self.backend = default_backend()
        self.key_manager = key_manager
        self.method_name = "aes-gcm-argon2"
    
    def encrypt(self, data: bytes, password: str, **kwargs) -> EncryptionResult:
        """
        Chiffre des données avec AES-GCM et Argon2
        
        Args:
            data: Données à chiffrer
            password: Mot de passe pour la dérivation de clé
            **kwargs: Paramètres optionnels (memory_cost, time_cost, parallelism)
        
        Returns:
            EncryptionResult: Résultat du chiffrement
        """
        try:
            # Paramètres Argon2 personnalisables
            memory_cost = kwargs.get('memory_cost', 65536)
            time_cost = kwargs.get('time_cost', 3)
            parallelism = kwargs.get('parallelism', 4)
            
            # Dérivation de la clé avec Argon2
            key_result = self.key_manager.derive_key_argon2(
                password=password,
                key_length=32,  # AES-256
                memory_cost=memory_cost,
                time_cost=time_cost,
                parallelism=parallelism
            )
            
            if not key_result.success:
                return EncryptionResult(
                    encrypted_data=b'',
                    metadata={},
                    method=self.method_name,
                    success=False,
                    error_message=key_result.error_message
                )
            
            # Génération d'un nonce aléatoire (12 octets recommandé pour AES-GCM)
            nonce = self.key_manager.generate_random_nonce(12)
            
            # Chiffrement avec AES-GCM
            aesgcm = AESGCM(key_result.key)
            encrypted_data = aesgcm.encrypt(nonce, data, None)
            
            # Métadonnées pour le déchiffrement
            metadata = {
                'method': self.method_name,
                'nonce': nonce.hex(),
                'salt': key_result.salt.hex(),
                'argon2_params': key_result.parameters,
                'algorithm': 'AES-256-GCM'
            }
            
            # Construction du résultat final
            final_data = {
                'encrypted_data': encrypted_data.hex(),
                'metadata': metadata
            }
            
            return EncryptionResult(
                encrypted_data=json.dumps(final_data).encode('utf-8'),
                metadata=metadata,
                method=self.method_name,
                success=True
            )
            
        except Exception as e:
            return EncryptionResult(
                encrypted_data=b'',
                metadata={},
                method=self.method_name,
                success=False,
                error_message=f"Erreur de chiffrement AES-GCM: {str(e)}"
            )
    
    def decrypt(self, encrypted_data: bytes, password: str, **kwargs) -> DecryptionResult:
        """
        Déchiffre des données avec AES-GCM et Argon2
        
        Args:
            encrypted_data: Données chiffrées
            password: Mot de passe pour la dérivation de clé
            **kwargs: Paramètres optionnels
        
        Returns:
            DecryptionResult: Résultat du déchiffrement
        """
        try:
            # Vérifier si les données sont en format JSON interne ou hexadécimal simple
            try:
                # Essayer de décoder comme JSON (format interne)
                encrypted_json = json.loads(encrypted_data.decode('utf-8'))
                ciphertext = bytes.fromhex(encrypted_json['encrypted_data'])
                metadata = encrypted_json['metadata']
            except (json.JSONDecodeError, KeyError, ValueError, UnicodeDecodeError):
                # Format hexadécimal simple - essayer de reconstruire les métadonnées
                # Dans ce cas, on ne peut pas déchiffrer sans nonce et salt
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message="Format hexadécimal non supporté pour AES-GCM - nécessite nonce et salt"
                )
            
            # Vérification de la méthode
            if metadata.get('method') != self.method_name:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Méthode incompatible: {metadata.get('method')}"
                )
            
            # Extraction des paramètres
            nonce = bytes.fromhex(metadata['nonce'])
            salt = bytes.fromhex(metadata['salt'])
            argon2_params = metadata['argon2_params']
            
            # Dérivation de la clé avec les mêmes paramètres
            key_result = self.key_manager.derive_key_argon2(
                password=password,
                salt=salt,
                key_length=argon2_params['key_length'],
                memory_cost=argon2_params['memory_cost'],
                time_cost=argon2_params['time_cost'],
                parallelism=argon2_params['parallelism']
            )
            
            if not key_result.success:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Erreur de dérivation de clé: {key_result.error_message}"
                )
            
            # Déchiffrement avec AES-GCM
            aesgcm = AESGCM(key_result.key)
            decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
            
            return DecryptionResult(
                decrypted_data=decrypted_data,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return DecryptionResult(
                decrypted_data=b'',
                metadata={},
                success=False,
                error_message=f"Erreur de déchiffrement AES-GCM: {str(e)}"
            )
    
    def get_method_name(self) -> str:
        """Retourne le nom de la méthode"""
        return self.method_name
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la méthode"""
        return {
            'name': self.method_name,
            'display_name': 'AES-GCM avec Argon2',
            'description': 'Chiffrement symétrique AES-256 en mode GCM avec dérivation de clé Argon2id',
            'security_level': 'Très élevé',
            'features': [
                'Authentification intégrée (AEAD)',
                'Protection contre les attaques par force brute (Argon2)',
                'Résistance à la modification des données',
                'Standard moderne et sécurisé'
            ],
            'recommended_use_cases': [
                'Fichiers sensibles',
                'Communication sécurisée',
                'Stockage à long terme'
            ]
        }