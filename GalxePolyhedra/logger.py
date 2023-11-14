from sys import stderr

from loguru import logger

logger.remove()

logger.add(stderr, format='<bold><white>{time:HH:mm:ss}</white></bold> | '
                          '<level>{level: <8}</level> | '
                          '<bold><level>{message}</level></bold>')

logger.add("Logs/logs.log", format='<bold><white>{time:HH:mm:ss}</white></bold> | '
                                   '<level>{level: <8}</level> | '
                                   '<bold><level>{message}</level></bold>')
