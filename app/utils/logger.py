import logging
import sys
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Formatter con colores para diferentes niveles de log"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"{color}[{timestamp}] [{record.levelname}]{reset} {record.getMessage()}"
        
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
            
        return formatted

def setup_logger():
    """Configura el logger de la aplicación"""
    logger = logging.getLogger("auth_api")
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def log_info(message: str, **kwargs):
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    full_message = f"{message} | {extra_info}" if extra_info else message
    logger.info(full_message)

def log_error(message: str, error: Exception = None, **kwargs):
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    full_message = f"{message} | {extra_info}" if extra_info else message
    
    if error:
        full_message += f" | Error: {str(error)}"
    
    logger.error(full_message)

def log_warning(message: str, **kwargs):
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    full_message = f"{message} | {extra_info}" if extra_info else message
    logger.warning(full_message)