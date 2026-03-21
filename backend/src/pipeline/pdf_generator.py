"""PDF export generator using fpdf2.

TODO: implement PDF rendering from Markdown content.
"""


def generate_pdf(markdown_content: str) -> bytes:
    """Generate a PDF from the Markdown report content.

    Uses fpdf2 (pure Python, no system dependencies).
    Returns raw PDF bytes for streaming download.
    """
    raise NotImplementedError("PDF generator not implemented yet")
