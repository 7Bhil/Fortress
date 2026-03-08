import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

class ValidationError(Exception):
    """Exception levée lors d'une erreur de validation"""
    pass

class FileValidator:
    """Validateur pour les opérations sur les fichiers"""
    
    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """Vérifie qu'un fichier existe"""
        if not os.path.exists(file_path):
            raise ValidationError(f"Le fichier {file_path} n'existe pas")
        return True
    
    @staticmethod
    def validate_file_readable(file_path: str) -> bool:
        """Vérifie qu'un fichier est lisible"""
        if not os.access(file_path, os.R_OK):
            raise ValidationError(f"Le fichier {file_path} n'est pas lisible")
        return True
    
    @staticmethod
    def validate_file_writable(file_path: str) -> bool:
        """Vérifie qu'un fichier est accessible en écriture"""
        dir_path = os.path.dirname(file_path) or "."
        if not os.access(dir_path, os.W_OK):
            raise ValidationError(f"Le répertoire {dir_path} n'est pas accessible en écriture")
        return True
    
    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: int = 100) -> bool:
        """Vérifie la taille maximale d'un fichier"""
        size_bytes = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if size_bytes > max_size_bytes:
            raise ValidationError(
                f"Le fichier {file_path} est trop volumineux: "
                f"{size_bytes / (1024*1024):.1f} Mo (max: {max_size_mb} Mo)"
            )
        return True
    
    @staticmethod
    def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> bool:
        """Vérifie l'extension d'un fichier"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in [ext.lower() for ext in allowed_extensions]:
            raise ValidationError(
                f"Extension non autorisée: {file_ext}. "
                f"Extensions autorisées: {', '.join(allowed_extensions)}"
            )
        return True
    
    @staticmethod
    def validate_encrypted_file(file_path: str) -> bool:
        """Valide le format d'un fichier chiffré"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Vérification des champs requis
            required_fields = ['version', 'method', 'metadata', 'encrypted_data']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Champ manquant dans le fichier chiffré: {field}")
            
            # Vérification du format des données chiffrées
            try:
                bytes.fromhex(data['encrypted_data'])
            except ValueError:
                raise ValidationError("Format invalide pour les données chiffrées")
            
            return True
            
        except json.JSONDecodeError:
            raise ValidationError("Le fichier n'est pas un JSON valide")
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Erreur lors de la validation du fichier: {str(e)}")

class PasswordValidator:
    """Validateur pour les mots de passe"""
    
    @staticmethod
    def validate_password_length(password: str, min_length: int = 8, max_length: int = 128) -> bool:
        """Valide la longueur d'un mot de passe"""
        if len(password) < min_length:
            raise ValidationError(f"Le mot de passe doit contenir au moins {min_length} caractères")
        
        if len(password) > max_length:
            raise ValidationError(f"Le mot de passe ne doit pas dépasser {max_length} caractères")
        
        return True
    
    @staticmethod
    def validate_password_complexity(password: str) -> Dict[str, Any]:
        """Évalue la complexité d'un mot de passe"""
        result = {
            'valid': True,
            'warnings': [],
            'score': 0,
            'checks': {
                'has_upper': bool(re.search(r'[A-Z]', password)),
                'has_lower': bool(re.search(r'[a-z]', password)),
                'has_digit': bool(re.search(r'\d', password)),
                'has_special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
                'no_common_patterns': not bool(re.search(r'(.)\1{2,}', password)),  # Pas 3+ caractères identiques
                'no_sequences': not PasswordValidator._has_sequences(password)
            }
        }
        
        # Calcul du score
        for check_name, passed in result['checks'].items():
            if passed:
                result['score'] += 1
        
        # Génération des avertissements
        if not result['checks']['has_upper']:
            result['warnings'].append("Ajoutez des majuscules")
        
        if not result['checks']['has_lower']:
            result['warnings'].append("Ajoutez des minuscules")
        
        if not result['checks']['has_digit']:
            result['warnings'].append("Ajoutez des chiffres")
        
        if not result['checks']['has_special']:
            result['warnings'].append("Ajoutez des caractères spéciaux")
        
        if not result['checks']['no_common_patterns']:
            result['warnings'].append("Évitez les répétitions de caractères")
        
        if not result['checks']['no_sequences']:
            result['warnings'].append("Évitez les suites de caractères")
        
        # Validation minimale
        if result['score'] < 3:
            result['valid'] = False
        
        return result
    
    @staticmethod
    def _has_sequences(password: str) -> bool:
        """Détecte les suites de caractères (abc, 123, etc.)"""
        # Suites communes à vérifier
        sequences = [
            'abcdefghijklmnopqrstuvwxyz',
            '0123456789',
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        password_lower = password.lower()
        
        for seq in sequences:
            for i in range(len(seq) - 2):
                subseq = seq[i:i+3]
                if subseq in password_lower:
                    return True
        
        return False
    
    @staticmethod
    def validate_common_passwords(password: str) -> bool:
        """Vérifie que le mot de passe n'est pas dans les mots de passe courants"""
        # Liste de mots de passe courants (simplifiée)
        common_passwords = {
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234567890', 'password1', 'qwerty123', 'admin123'
        }
        
        if password.lower() in common_passwords:
            raise ValidationError("Ce mot de passe est trop courant et non sécurisé")
        
        return True

class MethodValidator:
    """Validateur pour les méthodes de chiffrement"""
    
    @staticmethod
    def validate_method_name(method: str, available_methods: List[str]) -> bool:
        """Valide le nom d'une méthode de chiffrement"""
        if not method:
            raise ValidationError("Le nom de la méthode ne peut pas être vide")
        
        if method not in available_methods:
            raise ValidationError(
                f"Méthode '{method}' non disponible. "
                f"Méthodes disponibles: {', '.join(available_methods)}"
            )
        
        return True
    
    @staticmethod
    def validate_argon2_params(memory_cost: int, time_cost: int, parallelism: int) -> bool:
        """Valide les paramètres Argon2"""
        if memory_cost < 1024 or memory_cost > 2**31:
            raise ValidationError("memory_cost doit être entre 1024 et 2^31")
        
        if time_cost < 1 or time_cost > 2**31:
            raise ValidationError("time_cost doit être entre 1 et 2^31")
        
        if parallelism < 1 or parallelism > 2**24:
            raise ValidationError("parallelism doit être entre 1 et 2^24")
        
        return True
    
    @staticmethod
    def validate_key_size(key_size: int, algorithm: str) -> bool:
        """Valide la taille des clés"""
        valid_sizes = {
            'aes': [128, 192, 256],
            'rsa': [1024, 2048, 3072, 4096],
            'chacha20': [256]
        }
        
        if algorithm not in valid_sizes:
            raise ValidationError(f"Algorithme non reconnu: {algorithm}")
        
        if key_size not in valid_sizes[algorithm]:
            raise ValidationError(
                f"Taille de clé invalide pour {algorithm}: {key_size}. "
                f"Tailles valides: {valid_sizes[algorithm]}"
            )
        
        return True

class InputValidator:
    """Validateur général pour les entrées utilisateur"""
    
    @staticmethod
    def validate_non_empty_string(value: str, field_name: str = "valeur") -> bool:
        """Valide qu'une chaîne n'est pas vide"""
        if not value or not value.strip():
            raise ValidationError(f"Le champ {field_name} ne peut pas être vide")
        return True
    
    @staticmethod
    def validate_integer_range(value: int, min_val: int, max_val: int, field_name: str = "valeur") -> bool:
        """Valide qu'un entier est dans une plage"""
        if not isinstance(value, int):
            raise ValidationError(f"Le champ {field_name} doit être un entier")
        
        if value < min_val or value > max_val:
            raise ValidationError(
                f"Le champ {field_name} doit être entre {min_val} et {max_val}"
            )
        
        return True
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """Valide un chemin de fichier"""
        try:
            # Normalisation du chemin
            normalized_path = os.path.normpath(path)
            
            # Vérification des caractères invalides
            invalid_chars = '<>:"|?*' if os.name == 'nt' else '\0'
            for char in invalid_chars:
                if char in path:
                    raise ValidationError(f"Caractère invalide dans le chemin: {char}")
            
            return True
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Chemin invalide: {str(e)}")
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Nettoie un nom de fichier"""
        # Suppression des caractères invalides
        invalid_chars = '<>:"/\\|?*' if os.name == 'nt' else '\0/'
        sanitized = filename
        
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limitation de la longueur
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            max_name_len = 255 - len(ext)
            sanitized = name[:max_name_len] + ext
        
        return sanitized

class SecurityValidator:
    """Validateur spécifique à la sécurité"""
    
    @staticmethod
    def validate_secure_environment() -> Dict[str, Any]:
        """Valide que l'environnement est sécurisé"""
        results = {
            'secure': True,
            'warnings': [],
            'checks': {}
        }
        
        # Vérification des permissions du répertoire courant
        current_dir = os.getcwd()
        dir_stat = os.stat(current_dir)
        mode = oct(dir_stat.st_mode)[-3:]
        
        results['checks']['dir_permissions'] = mode
        if mode in ['777', '666']:
            results['warnings'].append("Le répertoire courant a des permissions trop permissives")
            results['secure'] = False
        
        # Vérification que nous ne sommes pas dans /tmp ou /var/tmp
        if current_dir.startswith('/tmp'):
            results['warnings'].append("Opération dans un répertoire temporaire")
            results['secure'] = False
        
        # Vérification de l'espace disque disponible
        statvfs = os.statvfs(current_dir)
        free_space = statvfs.f_frsize * statvfs.f_bavail
        free_space_mb = free_space / (1024 * 1024)
        
        results['checks']['free_space_mb'] = free_space_mb
        if free_space_mb < 100:  # Moins de 100 Mo
            results['warnings'].append(f"Espace disque faible: {free_space_mb:.1f} Mo")
        
        return results
    
    @staticmethod
    def validate_memory_usage(estimated_size: int, max_memory_mb: int = 512) -> bool:
        """Valide l'utilisation mémoire estimée"""
        max_memory_bytes = max_memory_mb * 1024 * 1024
        
        if estimated_size > max_memory_bytes:
            raise ValidationError(
                f"L'opération nécessite trop de mémoire: "
                f"{estimated_size / (1024*1024):.1f} Mo (max: {max_memory_mb} Mo)"
            )
        
        return True

# Fonctions de validation combinées
def validate_encryption_operation(file_path: str, password: str, method: str, 
                                available_methods: List[str]) -> bool:
    """Validation complète pour une opération de chiffrement"""
    FileValidator.validate_file_exists(file_path)
    FileValidator.validate_file_readable(file_path)
    FileValidator.validate_file_size(file_path)
    
    PasswordValidator.validate_password_length(password)
    PasswordValidator.validate_common_passwords(password)
    
    MethodValidator.validate_method_name(method, available_methods)
    
    return True

def validate_decryption_operation(file_path: str, password: str) -> bool:
    """Validation complète pour une opération de déchiffrement"""
    FileValidator.validate_file_exists(file_path)
    FileValidator.validate_file_readable(file_path)
    FileValidator.validate_encrypted_file(file_path)
    
    PasswordValidator.validate_password_length(password)
    
    return True