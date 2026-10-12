"""Response construction for thin ANPR results."""

import time

from app.schemas import PlateResult, RecognitionResponse


def _build_response(
    results: list[PlateResult],
    start_time: float,
) -> RecognitionResponse:
    """Assemble thin RecognitionResponse containing plate results with execution latency."""
    elapsed = round((time.time() - start_time) * 1000, 2)
    for r in results:
        r.execution_time_ms = elapsed
    return RecognitionResponse(
        results=results,
        execution_time_ms=elapsed,
    )
