term_escape = "\033"
yellow_code = "[33m"


def log(message, color_escape=term_escape + yellow_code):
    color_reset_escape = term_escape + "[0m"
    print(color_escape + message + color_reset_escape)
