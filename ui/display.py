import sys
from typing import Optional

class Colors:
    """Codes couleur ANSI pour l'affichage terminal"""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Couleurs de fond
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'

class DisplayManager:
    """Gestionnaire d'affichage avec couleurs et formatage"""
    
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Vérifie si le terminal supporte les couleurs"""
        # Vérification basique du support des couleurs
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            try:
                import curses
                curses.setupterm()
                return curses.tigetnum('colors') > 0
            except:
                return True
        return False
    
    def _colorize(self, text: str, color: str) -> str:
        """Applique une couleur au texte si supporté"""
        if self.use_colors:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def header(self, text: str):
        """Affiche un en-tête"""
        separator = "=" * 60
        print(f"\n{separator}")
        print(self._colorize(f"  {text}", Colors.BOLD + Colors.CYAN))
        print(f"{separator}\n")
    
    def success(self, text: str):
        """Affiche un message de succès"""
        print(f"{self._colorize('✓', Colors.GREEN)} {text}")
    
    def error(self, text: str):
        """Affiche un message d'erreur"""
        print(f"{self._colorize('✗', Colors.RED)} {text}", file=sys.stderr)
    
    def warning(self, text: str):
        """Affiche un avertissement"""
        print(f"{self._colorize('⚠', Colors.YELLOW)} {text}")
    
    def info(self, text: str):
        """Affiche un message d'information"""
        print(f"{self._colorize('ℹ', Colors.BLUE)} {text}")
    
    def code(self, text: str, language: str = ""):
        """Affiche du code formaté"""
        if language:
            print(self._colorize(f"```{language}", Colors.DIM))
        print(self._colorize(text, Colors.PURPLE))
        if language:
            print(self._colorize("```", Colors.DIM))
    
    def list_item(self, text: str, level: int = 0):
        """Affiche un élément de liste avec indentation"""
        indent = "  " * level
        print(f"{indent}• {text}")
    
    def progress(self, text: str, current: int, total: int):
        """Affiche une barre de progression simple"""
        percentage = (current / total) * 100
        bar_length = 30
        filled = int((current / total) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\r{self._colorize('▶', Colors.CYAN)} {text} [{bar}] {percentage:.1f}%", end="", flush=True)
        
        if current == total:
            print()  # Nouvelle ligne à la fin
    
    def table_row(self, columns: list, widths: list, headers: bool = False):
        """Affiche une ligne de tableau"""
        formatted_columns = []
        for i, (col, width) in enumerate(zip(columns, widths)):
            if headers:
                col = self._colorize(str(col).ljust(width), Colors.BOLD)
            else:
                col = str(col).ljust(width)
            formatted_columns.append(col)
        
        print("│ " + " │ ".join(formatted_columns) + " │")
    
    def table_separator(self, widths: list):
        """Affiche un séparateur de tableau"""
        separator = "├" + "┼".join(["─" * (w + 2) for w in widths]) + "┤"
        print(separator)
    
    def table_header(self, widths: list):
        """Affiche l'en-tête de tableau"""
        separator = "┌" + "┬".join(["─" * (w + 2) for w in widths]) + "┐"
        print(separator)
    
    def table_footer(self, widths: list):
        """Affiche le pied de tableau"""
        separator = "└" + "┴".join(["─" * (w + 2) for w in widths]) + "┘"
        print(separator)
    
    def box(self, text: str, title: str = "", style: str = "single"):
        """Affiche du texte dans une boîte"""
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        
        if title:
            max_length = max(max_length, len(title) + 4)
        
        # Choix des caractères selon le style
        if style == "double":
            h = "═"
            v = "║"
            tl = "╔"
            tr = "╗"
            bl = "╚"
            br = "╝"
            cross = "╬"
            left = "╠"
            right = "╣"
        else:  # single
            h = "─"
            v = "│"
            tl = "┌"
            tr = "┐"
            bl = "└"
            br = "┘"
            cross = "┼"
            left = "├"
            right = "┤"
        
        # Ligne supérieure
        top = tl + h * (max_length + 2) + tr
        print(self._colorize(top, Colors.CYAN))
        
        # Titre si présent
        if title:
            title_line = v + " " + self._colorize(title, Colors.BOLD) + " " * (max_length - len(title) + 1) + v
            print(title_line)
            separator = left + h * (max_length + 2) + right
            print(self._colorize(separator, Colors.CYAN))
        
        # Contenu
        for line in lines:
            content = v + " " + line.ljust(max_length) + " " + v
            print(content)
        
        # Ligne inférieure
        bottom = bl + h * (max_length + 2) + br
        print(self._colorize(bottom, Colors.CYAN))
    
    def step(self, step_num: int, total_steps: int, description: str):
        """Affiche une étape dans un processus"""
        print(f"{self._colorize(f'[{step_num}/{total_steps}]', Colors.CYAN)} {description}")
    
    def ask_yes_no(self, question: str, default: bool = False) -> bool:
        """Pose une question oui/non et retourne la réponse"""
        default_text = "O/n" if default else "o/N"
        prompt = f"{self._colorize('?', Colors.YELLOW)} {question} ({default_text}): "
        
        while True:
            response = input(prompt).lower().strip()
            
            if not response:
                return default
            
            if response in ['o', 'oui', 'yes', 'y']:
                return True
            elif response in ['n', 'non', 'no']:
                return False
            else:
                self.warning("Répondez par 'o' (oui) ou 'n' (non)")
    
    def ask_choice(self, question: str, choices: list, default: Optional[int] = None) -> int:
        """Demande à l'utilisateur de choisir parmi des options"""
        print(f"{self._colorize('?', Colors.YELLOW)} {question}")
        
        for i, choice in enumerate(choices, 1):
            marker = "→" if i - 1 == default else " "
            print(f"  {marker} {i}. {choice}")
        
        while True:
            prompt = "Choix: "
            if default is not None:
                prompt += f"[{default + 1}] "
            
            response = input(prompt).strip()
            
            if not response and default is not None:
                return default
            
            try:
                choice_num = int(response)
                if 1 <= choice_num <= len(choices):
                    return choice_num - 1
                else:
                    self.warning(f"Choisissez un nombre entre 1 et {len(choices)}")
            except ValueError:
                self.warning("Entrez un nombre valide")
    
    def spinner_start(self, text: str):
        """Démarre un spinner (simple, non-bloquant)"""
        # Pour l'instant, juste afficher le texte
        # Une implémentation complète utiliserait des threads
        print(f"{self._colorize('⏳', Colors.CYAN)} {text}...", end="", flush=True)
    
    def spinner_stop(self, success: bool = True):
        """Arrête le spinner"""
        if success:
            print(f" {self._colorize('✓', Colors.GREEN)}")
        else:
            print(f" {self._colorize('✗', Colors.RED)}")
    
    def clear_screen(self):
        """Efface l'écran du terminal"""
        print("\033[2J\033[H", end="")
    
    def new_line(self, count: int = 1):
        """Ajoute des lignes vides"""
        print("\n" * (count - 1))