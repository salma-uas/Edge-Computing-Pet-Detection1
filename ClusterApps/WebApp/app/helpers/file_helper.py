from pathlib import Path

def create_log_dir() -> None:
    """Creates Log Dir to avoid error if no Logs dir is created"""
    grand_par_dir = Path(__file__).resolve().parents[1]
    log_dir = grand_par_dir / "Logs"
    log_dir.mkdir(exist_ok=True)
    
def get_log_dir() -> Path:
    log_dir = Path(__file__).resolve().parents[1] / "Logs"
    
    return log_dir