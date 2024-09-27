import logging


def get_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:  # 핸들러가 없을 때만 설정
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')

        logger.setLevel(numeric_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
