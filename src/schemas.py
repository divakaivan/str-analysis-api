from dataclasses import dataclass
from pydantic import BaseModel, Field


class StrInput(BaseModel):
    """Input model for string analysis functionality"""

    str_input: str = Field(
        min_length=1,
        max_length=100_000,
        description="Input string to analyse (max 100,000 chars)",
        examples=["hello world (min 1, max 100,000 chars)"],
    )


class AnalysisResponse(BaseModel):
    """Response model for `POST /v1/analysis/:type`"""

    response: dict[str, str] = Field(
        description="Mapping of analysis type to that analysis result"
    )
    message: str = Field(description="A human-readable status message")
    request_id: str = Field(
        description="The X-Request-ID header value from the request"
    )


@dataclass
class AnalysesContext:
    api_key: str | None = None
