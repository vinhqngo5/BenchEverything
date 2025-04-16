import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# --- Logging Setup ---

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels."""
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "%(levelname)s: %(message)s" + Style.RESET_ALL,
        logging.INFO: "%(message)s",
        logging.WARNING: Fore.YELLOW + "WARNING: %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "ERROR: %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "CRITICAL: %(message)s" + Style.RESET_ALL
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

_logger_instance = None

def setup_logger(name="BenchEverything", level=logging.INFO):
    """Configure and return a colored logger instance."""
    global _logger_instance
    if _logger_instance:
        return _logger_instance

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if called again
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)

    _logger_instance = logger
    return logger

def get_logger():
    """Get the pre-configured logger instance."""
    if not _logger_instance:
        return setup_logger()
    return _logger_instance

# Ensure logger is set up when the module is imported
get_logger()