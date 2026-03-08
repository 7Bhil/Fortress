import os
import json
import hmac
import hashlib
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from core.crypto_engine import CryptoMethod, EncryptionResult, DecryptionResult
from core.key_manager import key_manager

class AESCBCMACMethod(CryptoMethod):
    """Implémentation du chiffrement AES-CBC avec HMAC-SHA256"""
    
    def __init__(self):
        self.backend = default_backend()
        self.key_manager = key_manager
        self.method_name = "aes-cbc-hmac"
    
    def encrypt(self, data: bytes, password: str, **kwargs) -> EncryptionResult:
        """
        Chiffre des données avec AES-CBC et HMAC-SHA256
        
        Args:
            data: Données à chiffrer
            password: Mot de passe pour la dérivation de clé
            **kwargs: Paramètres optionnels
        
        Returns:
            EncryptionResult: Résultat du chiffrement
        """
        try:
            # Dérivation de la clé principale avec PBKDF2
            key_result = self.key_manager.derive_key_pbkdf2(
                password=password,
                key_length=64,  # 32 octets pour AES + 32 octets pour HMAC
                iterations=kwargs.get('iterations', 100000)
            )
            
            if not key_result.success:
                return EncryptionResult(
                    encrypted_data=b'',
                    metadata={},
                    method=self.method_name,
                    success=False,
                    error_message=key_result.error_message
                )
            
            # Séparation des clés
            aes_key = key_result.key[:32]  # Premiers 32 octets pour AES-256
            hmac_key = key_result.key[32:]  # Derniers 32 octets pour HMAC
            
            # Génération d'un IV aléatoire (16 octets pour AES)
            iv = self.key_manager.generate_random_iv(16)
            
            # Padding PKCS7 pour AES-CBC
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            
            # Chiffrement AES-CBC
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # Calcul du HMAC sur (IV + données chiffrées)
            hmac_obj = hmac.new(hmac_key, iv + encrypted_data, hashlib.sha256)
            hmac_signature = hmac_obj.digest()
            
            # Métadonnées pour le déchiffrement
            metadata = {
                'method': self.method_name,
                'iv': iv.hex(),
                'salt': key_result.salt.hex(),
                'pbkdf2_params': key_result.parameters,
                'hmac': hmac_signature.hex(),
                'algorithm': 'AES-256-CBC + HMAC-SHA256'
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
                error_message=f"Erreur de chiffrement AES-CBC: {str(e)}"
            )
    
    def decrypt(self, encrypted_data: bytes, password: str, **kwargs) -> DecryptionResult:
        """
        Déchiffre des données avec AES-CBC et HMAC-SHA256
        
        Args:
            encrypted_data: Données chiffrées
            password: Mot de passe pour la dérivation de clé
            **kwargs: Paramètres optionnels
        
        Returns:
            DecryptionResult: Résultat du déchiffrement
        """
        try:
            # Parsing des données chiffrées
            try:
                encrypted_json = json.loads(encrypted_data.decode('utf-8'))
                ciphertext = bytes.fromhex(encrypted_json['encrypted_data'])
                metadata = encrypted_json['metadata']
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Format de données invalide: {str(e)}"
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
            iv = bytes.fromhex(metadata['iv'])
            salt = bytes.fromhex(metadata['salt'])
            stored_hmac = bytes.fromhex(metadata['hmac'])
            pbkdf2_params = metadata['pbkdf2_params']
            
            # Dérivation de la clé avec les mêmes paramètres
            key_result = self.key_manager.derive_key_pbkdf2(
                password=password,
                salt=salt,
                key_length=pbkdf2_params['key_length'],
                iterations=pbkdf2_params['iterations']
            )
            
            if not key_result.success:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=key_result.error_message
                )
            
            # Séparation des clés
            aes_key = key_result.key[:32]
            hmac_key = key_result.key[32:]
            
            # Vérification du HMAC
            hmac_obj = hmac.new(hmac_key, iv + ciphertext, hashlib.sha256)
            calculated_hmac = hmac_obj.digest()
            
            if not hmac.compare_digest(stored_hmac, calculated_hmac):
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message="Erreur d'authentification: les données ont été modifiées ou le mot de passe est incorrect"
                )
            
            # Déchiffrement AES-CBC
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Retrait du padding PKCS7
            unpadder = padding.PKCS7(128).unpadder()
            try:
                data = unpadder.update(padded_data) + unpadder.finalize()
            except ValueError as e:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Erreur de padding: données corrompues {str(e)}"
                )
            
            return DecryptionResult(
                decrypted_data=data,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return DecryptionResult(
                decrypted_data=b'',
                metadata={},
                success=False,
                error_message=f"Erreur de déchiffrement AES-CBC: {str(e)}"
            )
    
    def get_method_name(self) -> str:
        """Retourne le nom de la méthode"""
        return self.method_name
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la méthode"""
        return {
            'name': self.method_name,
            'display_name': 'AES-CBC avec HMAC',
            'description': 'Chiffrement symétrique AES-256 en mode CBC avec authentification HMAC-SHA256',
            'security_level': 'Élevé',
            'features': [
                'Authentification séparée (HMAC)',
                'Standard éprouvé et largement utilisé',
                'Protection contre la modification des données',
                'Compatible avec de nombreux systèmes'
            ],
            'recommended_use_cases': [
                'Compatibilité avec systèmes existants',
                'Fichiers de taille moyenne à grande',
                'Applications nécessitant un standard éprouvé'
            ]
        }