from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(message: str):
    print(f"[{datetime.today().strftime('%H:%M:%S %d-%m-%Y')}] {Colors.WARNING}{message}{Colors.ENDC}")