"""Markdown export generator.

Produces the frozen MD schema defined in contracts/export-schema.md.
Score MUST appear as: Score: {n}/100
"""

from src.models.report import AnalysisReport


def generate_markdown(report: AnalysisReport) -> str:
    """Generate a Markdown report following the frozen export schema.

    See contracts/export-schema.md for the exact schema contract.
    The score line MUST be exactly 'Score: {n}/100' (machine-parsable).
    """
    raise NotImplementedError("Markdown export generator not implemented yet")
