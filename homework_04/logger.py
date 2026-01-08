import logging

DEFAULT_LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format=DEFAULT_LOG_FORMAT,
)
log = logging.getLogger(__name__)
