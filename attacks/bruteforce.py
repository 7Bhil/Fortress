import itertools
import string
import time
import json
from typing import List, Dict, Any, Optional, Generator
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

@dataclass
class BruteForceResult:
    """Résultat d'une attaque par force brute"""
    success: bool
    password: Optional[str] = None
    attempts: int = 0
    duration: float = 0.0
    rate: float = 0.0  # mots de passe par seconde
    error_message: Optional[str] = None

class BruteForceAttack:
    """Simulateur d'attaque par force brute pour tests de sécurité"""
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.current_password = None
        self.attempts = 0
        self.start_time = None
    
    def generate_passwords(self, charset: str, min_length: int, max_length: int) -> Generator[str, None, None]:
        """Générateur de mots de passe par force brute"""
        for length in range(min_length, max_length + 1):
            for combination in itertools.product(charset, repeat=length):
                if self.stop_event.is_set():
                    break
                yield ''.join(combination)
    
    def generate_dictionary_passwords(self, dictionary: List[str], variations: bool = True) -> Generator[str, None, None]:
        """Générateur de mots de passe à partir d'un dictionnaire"""
        for word in dictionary:
            if self.stop_event.is_set():
                break
            
            yield word
            
            if variations:
                # Variations communes
                yield word.capitalize()
                yield word.upper()
                yield word + '1'
                yield word + '123'
                yield word + '2023'
                yield word + '2024'
                yield '1' + word
                yield '123' + word
    
    def test_password(self, encrypted_file: str, password: str, crypto_engine) -> bool:
        """Teste un mot de passe contre un fichier chiffré"""
        try:
            result = crypto_engine.decrypt_file(encrypted_file, password)
            return result.success
        except Exception:
            return False
    
    def attack_sequential(self, encrypted_file: str, charset: str, min_length: int, 
                         max_length: int, crypto_engine, max_attempts: Optional[int] = None) -> BruteForceResult:
        """Attaque par force brute séquentielle"""
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            for password in self.generate_passwords(charset, min_length, max_length):
                if self.stop_event.is_set():
                    break
                
                if max_attempts and self.attempts >= max_attempts:
                    break
                
                self.current_password = password
                self.attempts += 1
                
                if self.test_password(encrypted_file, password, crypto_engine):
                    duration = time.time() - self.start_time
                    rate = self.attempts / duration if duration > 0 else 0
                    
                    return BruteForceResult(
                        success=True,
                        password=password,
                        attempts=self.attempts,
                        duration=duration,
                        rate=rate
                    )
                
                # Affichage de la progression chaque 1000 tentatives
                if self.attempts % 1000 == 0:
                    duration = time.time() - self.start_time
                    rate = self.attempts / duration if duration > 0 else 0
                    print(f"\rTentatives: {self.attempts:,} | Rate: {rate:.1f}/sec | Actuel: {password}", end="", flush=True)
            
        except KeyboardInterrupt:
            print("\nAttaque interrompue par l'utilisateur")
        
        duration = time.time() - self.start_time
        rate = self.attempts / duration if duration > 0 else 0
        
        return BruteForceResult(
            success=False,
            attempts=self.attempts,
            duration=duration,
            rate=rate,
            error_message="Mot de passe non trouvé dans l'espace de recherche"
        )
    
    def attack_dictionary(self, encrypted_file: str, dictionary: List[str], 
                         crypto_engine, variations: bool = True, 
                         max_attempts: Optional[int] = None) -> BruteForceResult:
        """Attaque par dictionnaire"""
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            for password in self.generate_dictionary_passwords(dictionary, variations):
                if self.stop_event.is_set():
                    break
                
                if max_attempts and self.attempts >= max_attempts:
                    break
                
                self.current_password = password
                self.attempts += 1
                
                if self.test_password(encrypted_file, password, crypto_engine):
                    duration = time.time() - self.start_time
                    rate = self.attempts / duration if duration > 0 else 0
                    
                    return BruteForceResult(
                        success=True,
                        password=password,
                        attempts=self.attempts,
                        duration=duration,
                        rate=rate
                    )
                
                # Affichage de la progression
                if self.attempts % 100 == 0:
                    duration = time.time() - self.start_time
                    rate = self.attempts / duration if duration > 0 else 0
                    print(f"\rTentatives: {self.attempts:,} | Rate: {rate:.1f}/sec | Actuel: {password}", end="", flush=True)
            
        except KeyboardInterrupt:
            print("\nAttaque interrompue par l'utilisateur")
        
        duration = time.time() - self.start_time
        rate = self.attempts / duration if duration > 0 else 0
        
        return BruteForceResult(
            success=False,
            attempts=self.attempts,
            duration=duration,
            rate=rate,
            error_message="Mot de passe non trouvé dans le dictionnaire"
        )
    
    def attack_parallel(self, encrypted_file: str, charset: str, min_length: int, 
                       max_length: int, crypto_engine, num_threads: int = 4,
                       max_attempts: Optional[int] = None) -> BruteForceResult:
        """Attaque par force brute parallèle"""
        self.start_time = time.time()
        self.attempts = 0
        
        def worker_thread(password_batch):
            """Thread worker pour tester des lots de mots de passe"""
            local_attempts = 0
            for password in password_batch:
                if self.stop_event.is_set():
                    break
                
                if max_attempts and self.attempts + local_attempts >= max_attempts:
                    break
                
                if self.test_password(encrypted_file, password, crypto_engine):
                    return password, local_attempts + 1
                
                local_attempts += 1
            
            return None, local_attempts
        
        try:
            # Génération des lots de mots de passe
            password_generator = self.generate_passwords(charset, min_length, max_length)
            batch_size = 1000
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                
                while not self.stop_event.is_set():
                    # Création d'un lot
                    batch = []
                    for _ in range(batch_size):
                        try:
                            batch.append(next(password_generator))
                        except StopIteration:
                            break
                    
                    if not batch:
                        break
                    
                    # Soumission du lot
                    future = executor.submit(worker_thread, batch)
                    futures.append(future)
                    
                    # Limitation du nombre de futures en cours
                    if len(futures) >= num_threads * 2:
                        completed = as_completed(futures[:1])
                        for future in completed:
                            password, attempts = future.result()
                            self.attempts += attempts
                            
                            if password:
                                self.stop_event.set()
                                duration = time.time() - self.start_time
                                rate = self.attempts / duration if duration > 0 else 0
                                
                                return BruteForceResult(
                                    success=True,
                                    password=password,
                                    attempts=self.attempts,
                                    duration=duration,
                                    rate=rate
                                )
                            
                            futures.remove(future)
                
                # Traitement des futures restantes
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    
                    password, attempts = future.result()
                    self.attempts += attempts
                    
                    if password:
                        duration = time.time() - self.start_time
                        rate = self.attempts / duration if duration > 0 else 0
                        
                        return BruteForceResult(
                            success=True,
                            password=password,
                            attempts=self.attempts,
                            duration=duration,
                            rate=rate
                        )
        
        except KeyboardInterrupt:
            print("\nAttaque interrompue par l'utilisateur")
            self.stop_event.set()
        
        duration = time.time() - self.start_time
        rate = self.attempts / duration if duration > 0 else 0
        
        return BruteForceResult(
            success=False,
            attempts=self.attempts,
            duration=duration,
            rate=rate,
            error_message="Mot de passe non trouvé dans l'espace de recherche"
        )
    
    def stop(self):
        """Arrête l'attaque en cours"""
        self.stop_event.set()
    
    def estimate_cracking_time(self, charset_size: int, password_length: int, 
                             rate_per_second: float) -> Dict[str, Any]:
        """Estime le temps de cassage d'un mot de passe"""
        total_combinations = charset_size ** password_length
        
        # Calcul en secondes
        time_seconds = total_combinations / rate_per_second
        
        # Conversion en unités compréhensibles
        time_units = [
            ('années', 365.25 * 24 * 3600),
            ('mois', 30.44 * 24 * 3600),
            ('jours', 24 * 3600),
            ('heures', 3600),
            ('minutes', 60),
            ('secondes', 1)
        ]
        
        for unit_name, unit_seconds in time_units:
            if time_seconds >= unit_seconds:
                time_value = time_seconds / unit_seconds
                break
        else:
            time_value = time_seconds
            unit_name = 'secondes'
        
        return {
            'total_combinations': total_combinations,
            'time_seconds': time_seconds,
            'time_value': time_value,
            'time_unit': unit_name,
            'feasible': time_seconds < 365.25 * 24 * 3600  # Moins d'un an
        }
    
    def get_common_charsets(self) -> Dict[str, str]:
        """Retourne les jeux de caractères courants"""
        return {
            'digits': string.digits,
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'letters': string.ascii_letters,
            'alphanumeric': string.ascii_letters + string.digits,
            'common_symbols': '!@#$%^&*',
            'all_symbols': string.punctuation,
            'all_chars': string.printable.replace('\t', '').replace('\n', '').replace('\r', '')
        }
    
    def analyze_password_strength(self, password: str, rate_per_second: float = 1000000) -> Dict[str, Any]:
        """Analyse la force d'un mot de passe"""
        # Détermination du jeu de caractères utilisé
        charsets = self.get_common_charsets()
        charset_size = 0
        used_charsets = []
        
        for charset_name, charset in charsets.items():
            if any(c in charset for c in password):
                charset_size = max(charset_size, len(charset))
                used_charsets.append(charset_name)
        
        # Estimation du temps de cassage
        estimate = self.estimate_cracking_time(charset_size, len(password), rate_per_second)
        
        # Score de force
        if estimate['time_seconds'] < 60:
            strength = 'Très faible'
            score = 1
        elif estimate['time_seconds'] < 3600:
            strength = 'Faible'
            score = 2
        elif estimate['time_seconds'] < 24 * 3600:
            strength = 'Moyen'
            score = 3
        elif estimate['time_seconds'] < 365.25 * 24 * 3600:
            strength = 'Fort'
            score = 4
        else:
            strength = 'Très fort'
            score = 5
        
        return {
            'password': password,
            'length': len(password),
            'charset_size': charset_size,
            'used_charsets': used_charsets,
            'strength': strength,
            'score': score,
            'cracking_estimate': estimate
        }

# Fonctions utilitaires
def load_common_passwords(file_path: Optional[str] = None) -> List[str]:
    """Charge une liste de mots de passe courants"""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    
    # Liste par défaut (courte pour démonstration)
    return [
        'password', '123456', '123456789', 'qwerty', 'abc123',
        'password123', 'admin', 'letmein', 'welcome', 'monkey',
        '1234567890', 'password1', 'qwerty123', 'admin123',
        'root', 'toor', 'pass', 'test', 'guest', 'user'
    ]

def create_test_dictionary(output_file: str = "test_dictionary.txt"):
    """Crée un dictionnaire de test"""
    common_passwords = load_common_passwords()
    
    # Ajout de variations
    extended_passwords = set(common_passwords)
    
    for pwd in common_passwords:
        extended_passwords.add(pwd.capitalize())
        extended_passwords.add(pwd.upper())
        extended_passwords.add(pwd + '1')
        extended_passwords.add(pwd + '123')
        extended_passwords.add('1' + pwd)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for pwd in sorted(extended_passwords):
            f.write(pwd + '\n')
    
    print(f"Dictionnaire créé: {output_file} ({len(extended_passwords)} entrées)")

if __name__ == '__main__':
    # Test du module
    attack = BruteForceAttack()
    
    # Test d'analyse de force
    test_passwords = ['password', 'Password123!', 'MySuperSecurePassword2024!']
    
    print("Analyse de force de mots de passe:")
    for pwd in test_passwords:
        analysis = attack.analyze_password_strength(pwd)
        print(f"\nMot de passe: {pwd}")
        print(f"Force: {analysis['strength']} ({analysis['score']}/5)")
        print(f"Temps de cassage estimé: {analysis['cracking_estimate']['time_value']:.1f} {analysis['cracking_estimate']['time_unit']}")
    
    # Création d'un dictionnaire de test
    create_test_dictionary()