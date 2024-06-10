import logging

logger = logging.getLogger('lot_logger')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('lot_end.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
