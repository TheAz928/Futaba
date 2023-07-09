import logging

# Define ANSI escape sequences for colors
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = (
	f"\033[{i}m" for i in range(30, 38)
)
GRAY = '\033[90m'
RESET = '\033[0m'

# Define a dictionary mapping log levels to colors
level_colors = {
	logging.DEBUG   : CYAN,
	logging.INFO    : GREEN,
	logging.WARNING : YELLOW,
	logging.ERROR   : RED,
	logging.CRITICAL: MAGENTA,
}

formatter = logging.Formatter(f"{BLUE}[%(asctime)s] %(levelname)-8s"f"{BLACK}%(name_color)s %(name)-10s{RESET}{GRAY} %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class ColoredStreamHandler(logging.StreamHandler):
	def emit(self, record):
		try:
			# Add color to the log level name
			record.levelname = f"{level_colors[record.levelno]}{record.levelname}{RESET}"
			
			# Add color to the logger name
			name_color = WHITE
			record.name_color = name_color
			super().emit(record)
		except Exception:
			self.handleError(record)
   
_logger = logging.getLogger("BOT")
_logger.setLevel(logging.DEBUG)

# Create a terminal handler with the formatted output
_handler = ColoredStreamHandler()
_handler.setFormatter(formatter)

_logger.addHandler(_handler)

def get_logger() -> logging.Logger:
	return _logger