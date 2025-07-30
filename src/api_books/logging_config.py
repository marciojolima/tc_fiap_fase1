import sys

from loguru import logger

# Remove o handler padrão para ter
# controle total sobre a configuração.
logger.remove()

# --- Configuração do Logger para o CONSOLE ---
logger.add(
    sys.stdout,  # Envia logs para a saída padrão
    level='INFO',
    format=(
        '<green>{time:DD/MM/YYYY HH:mm:ss}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>'
    ),
    colorize=True,
)

# --- Configuração do Logger para ARQUIVO ---
# O caminho "logs/api_requests.log"
logger.add(
    'logs/api_requests.log',
    level='INFO',
    format=(
        '{time:DD/MM/YYYY HH:mm:ss} | {level: <8} | '
        '{extra[ip]} | {extra[method]}-{extra[url]: <50} | {extra[status_code]} | '
        'process_time: {extra[process_time]:.2f}ms'
    ),
    rotation='5 MB',  # Cria um novo arquivo quando o atual atingir 5 MB.
    retention='30 days',
    compression='zip', 
    enqueue=True,  # Torna o log assíncrono para não bloquear a thread principal
    backtrace=True,  # Mostra o stacktrace completo em caso de erros.
    diagnose=True,  # Adiciona informações de diagnóstico em exceções.
)

# Exporta a instância do logger configurado para ser usada em outras partes da aplicação
app_logger = logger
