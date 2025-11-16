import os

import re
import pyfiglet
from termcolor import colored

# Regex to remove ANSI escape codes (color codes) for accurate length calculation
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


def center_text(text: str, fill_char: str = ' ', width: int = None) -> str:
    """Centers the given text based on terminal width, accounting for double-width characters AND color codes."""
    if width is None:
        try:
            width = os.get_terminal_size().columns
        except OSError:
            width = 80  # Fallback width

    # 1. Strip ANSI escape codes to get the clean text for length calculation
    clean_text = ANSI_ESCAPE.sub('', text)

    # 2. Calculate the visual width (accounting for emojis)
    visual_length = 0
    for char in clean_text:
        # Simple heuristic: treat non-ASCII characters (which includes most emojis) as double-width
        if ord(char) > 127:
            visual_length += 2
        else:
            visual_length += 1

    # 3. Calculate the padding needed based on visual length
    padding = width - visual_length
    if padding <= 0:
        return text  # No centering needed

    left_pad = padding // 2
    right_pad = padding - left_pad

    # Apply padding to the original text (which still contains color codes)
    return fill_char * left_pad + text + fill_char * right_pad


def print_centered(text: str, color: str = None, attrs: list = None, on_color: str = None):
    """Prints a single line of text centered with optional color/attributes."""
    # Ensure on_color is ignored as per user request
    if on_color:
        on_color = None

    # Apply color first so center_text can strip the codes correctly
    if color or attrs or on_color:
        colored_text = colored(text, color, on_color, attrs=attrs)
    else:
        colored_text = text

    centered_line = center_text(colored_text)
    print(centered_line)


def print_centered_title(text: str, font: str, color: str = 'green', on_color: str = None, attrs: list = None):
    """Generates ASCII art and prints it centered line by line, allowing for a background color."""
    fig = pyfiglet.Figlet(font=font)
    rendered_text = fig.renderText(text)

    # Center each line of the ASCII art individually
    for line in rendered_text.splitlines():
        print_centered(line, color, attrs=attrs, on_color=on_color)