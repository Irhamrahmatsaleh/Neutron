import html

def sanitize_input(user_input: str) -> str:
    return html.escape(user_input)
