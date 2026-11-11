"""Bitácora: solo registra eventos y errores, sin persistir datos del negocio."""

import logging
from pathlib import Path


def crear_registro() -> logging.Logger:
    """Prepara un log local en UTF-8 sin duplicar manejadores."""
    carpeta = Path(__file__).resolve().parent.parent / "logs"
    carpeta.mkdir(exist_ok=True)
    archivo = carpeta / "software_fj.log"
    logger = logging.getLogger("software_fj")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        manejador = logging.FileHandler(archivo, encoding="utf-8")
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(manejador)
    return logger


registro = crear_registro()
