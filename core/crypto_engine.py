import os
import json
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class EncryptionResult:
    """Résultat d'une opération de chiffrement"""
    encrypted_data: bytes
    metadata: Dict[str, Any]
    method: str
    success: bool
    error_message: Optional[str] = None

@dataclass
class DecryptionResult:
    """Résultat d'une opération de déchiffrement"""
    decrypted_data: bytes
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

class CryptoMethod(ABC):
    """Classe abstraite pour les méthodes de chiffrement"""
    
    @abstractmethod
    def encrypt(self, data: bytes, password: str, **kwargs) -> EncryptionResult:
        """Chiffre les données avec un mot de passe"""
        pass
    
    @abstractmethod
    def decrypt(self, encrypted_data: bytes, password: str, **kwargs) -> DecryptionResult:
        """Déchiffre les données avec un mot de passe"""
        pass
    
    @abstractmethod
    def get_method_name(self) -> str:
        """Retourne le nom de la méthode"""
        pass

class CryptoEngine:
    """Moteur principal de chiffrement"""
    
    def __init__(self):
        self.methods: Dict[str, CryptoMethod] = {}
        self._register_default_methods()
    
    def _register_default_methods(self):
        """Enregistre les méthodes de chiffrement par défaut"""
        try:
            from methods.aes_gcm_argon2 import AESGCMArgon2Method
            self.register_method(AESGCMArgon2Method())
        except ImportError:
            pass
        
        try:
            from methods.aes_cbc_hmac import AESCBCMACMethod
            self.register_method(AESCBCMACMethod())
        except ImportError:
            pass
        
        try:
            from methods.chacha20_poly1305 import ChaCha20Poly1305Method
            self.register_method(ChaCha20Poly1305Method())
        except ImportError:
            pass
    
    def register_method(self, method: CryptoMethod):
        """Enregistre une nouvelle méthode de chiffrement"""
        self.methods[method.get_method_name()] = method
    
    def get_available_methods(self) -> list[str]:
        """Retourne la liste des méthodes disponibles"""
        return list(self.methods.keys())
    
    def encrypt_file(self, file_path: str, password: str, method: str, 
                    output_path: Optional[str] = None, **kwargs) -> EncryptionResult:
        """Chiffre un fichier"""
        try:
            if not os.path.exists(file_path):
                return EncryptionResult(
                    encrypted_data=b'',
                    metadata={},
                    method=method,
                    success=False,
                    error_message=f"Fichier introuvable: {file_path}"
                )
            
            if method not in self.methods:
                return EncryptionResult(
                    encrypted_data=b'',
                    metadata={},
                    method=method,
                    success=False,
                    error_message=f"Méthode non disponible: {method}"
                )
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Calcul du hash du fichier original pour vérification
            file_hash = hashlib.sha256(file_data).hexdigest()
            
            # Chiffrement
            crypto_method = self.methods[method]
            result = crypto_method.encrypt(file_data, password, **kwargs)
            
            if result.success:
                # Ajout des métadonnées du fichier
                result.metadata.update({
                    'original_filename': os.path.basename(file_path),
                    'original_size': len(file_data),
                    'original_hash': file_hash,
                    'file_extension': os.path.splitext(file_path)[1]
                })
                
                # Sauvegarde du fichier chiffré
                if output_path is None:
                    output_path = f"{file_path}.enc"
                
                self._save_encrypted_file(output_path, result)
            
            return result
            
        except Exception as e:
            return EncryptionResult(
                encrypted_data=b'',
                metadata={},
                method=method,
                success=False,
                error_message=f"Erreur lors du chiffrement: {str(e)}"
            )
    
    def decrypt_file(self, encrypted_file_path: str, password: str, 
                    output_path: Optional[str] = None) -> DecryptionResult:
        """Déchiffre un fichier"""
        try:
            if not os.path.exists(encrypted_file_path):
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Fichier introuvable: {encrypted_file_path}"
                )
            
            # Chargement du fichier chiffré
            encrypted_data, metadata, method = self._load_encrypted_file(encrypted_file_path)
            
            if method not in self.methods:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Méthode non disponible: {method}"
                )
            
            # Déchiffrement
            crypto_method = self.methods[method]
            result = crypto_method.decrypt(encrypted_data, password)
            
            if result.success:
                # Vérification de l'intégrité
                if 'original_hash' in metadata:
                    calculated_hash = hashlib.sha256(result.decrypted_data).hexdigest()
                    if calculated_hash != metadata['original_hash']:
                        return DecryptionResult(
                            decrypted_data=b'',
                            metadata={},
                            success=False,
                            error_message="Erreur d'intégrité: le fichier a été modifié"
                        )
                
                # Sauvegarde du fichier déchiffré
                if output_path is None:
                    original_name = metadata.get('original_filename', 'decrypted_file')
                    output_path = f"decrypted_{original_name}"
                
                with open(output_path, 'wb') as f:
                    f.write(result.decrypted_data)
                
                result.metadata = metadata
            
            return result
            
        except Exception as e:
            return DecryptionResult(
                decrypted_data=b'',
                metadata={},
                success=False,
                error_message=f"Erreur lors du déchiffrement: {str(e)}"
            )
    
    def encrypt_data(self, data: bytes, password: str, method: str, **kwargs) -> EncryptionResult:
        """Chiffre des données brutes"""
        try:
            if method not in self.methods:
                return EncryptionResult(
                    encrypted_data=b'',
                    metadata={},
                    method=method,
                    success=False,
                    error_message=f"Méthode non disponible: {method}"
                )
            
            crypto_method = self.methods[method]
            return crypto_method.encrypt(data, password, **kwargs)
            
        except Exception as e:
            return EncryptionResult(
                encrypted_data=b'',
                metadata={},
                method=method,
                success=False,
                error_message=f"Erreur lors du chiffrement: {str(e)}"
            )
    
    def decrypt_data(self, encrypted_data: bytes, password: str, 
                    metadata: Dict[str, Any]) -> DecryptionResult:
        """Déchiffre des données brutes"""
        try:
            method = metadata.get('method')
            if not method or method not in self.methods:
                return DecryptionResult(
                    decrypted_data=b'',
                    metadata={},
                    success=False,
                    error_message=f"Méthode non spécifiée ou non disponible: {method}"
                )
            
            crypto_method = self.methods[method]
            return crypto_method.decrypt(encrypted_data, password)
            
        except Exception as e:
            return DecryptionResult(
                decrypted_data=b'',
                metadata={},
                success=False,
                error_message=f"Erreur lors du déchiffrement: {str(e)}"
            )
    
    def _save_encrypted_file(self, file_path: str, result: EncryptionResult):
        """Sauvegarde un fichier chiffré avec métadonnées"""
        file_data = {
            'version': '1.0',
            'method': result.method,
            'metadata': result.metadata,
            'encrypted_data': result.encrypted_data.hex()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(file_data, f, indent=2)
    
    def _load_encrypted_file(self, file_path: str) -> Tuple[bytes, Dict[str, Any], str]:
        """Charge un fichier chiffré avec métadonnées"""
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        encrypted_data = bytes.fromhex(file_data['encrypted_data'])
        metadata = file_data.get('metadata', {})
        method = file_data.get('method', 'unknown')
        
        return encrypted_data, metadata, method

# Instance globale du moteur
crypto_engine = CryptoEngine()