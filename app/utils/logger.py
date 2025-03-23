import logging

def setup_logger(log_filename="log.txt"):
    logging.basicConfig(
        filename=log_filename,
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG
    )

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    return logger