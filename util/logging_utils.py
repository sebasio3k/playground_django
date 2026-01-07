import logging
from datetime import datetime
from zoneinfo import ZoneInfo


class LocalTimeFormatter(logging.Formatter):
    """
    Muestra el timestamp de los logs en zona horaria local,
    sin cambiar que Django trabaje en UTC internamente.
    """

    def __init__(self, *args, **kwargs):
        # Ajusta a tu zona: America/Mexico_City, etc.
        self.tz = ZoneInfo("America/Mexico_City")
        super().__init__(*args, **kwargs)

    def formatTime(self, record, datefmt=None):
        # record.created es un timestamp en segundos (UTC)
        dt = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        # fallback por si no se define datefmt
        return dt.isoformat(timespec="seconds")
