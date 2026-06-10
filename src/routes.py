from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
    Query,
    status,
)
from fastapi.responses import JSONResponse
from loguru import logger
from src.schemas import StrInput, AnalysisResponse, AnalysesContext
from src.analyzers.setup import get_model_api_key
from src.analyzers.base import AnalysesTypes

ROUTER = APIRouter()


@ROUTER.get("/v1/healthz", summary="Check the health of the server", tags=["health"])
def healthz():
    """Health check endpoint"""
    logger.info("healthz requested")
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)


@ROUTER.post(
    "/v1/analyses",
    summary="Run one or more analyses on text",
    tags=["analyses"],
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful analyses",
                            "value": {
                                "response": {
                                    "word_count": "42",
                                    "semantic": "The text discusses machine learning concepts.",
                                },
                                "message": "ok",
                                "request_id": "abc-123",
                            },
                        }
                    }
                }
            }
        },
        422: {
            "description": "Invalid request",
            "content": {
                "application/json": {
                    "examples": {
                        "str_input_too_long": {
                            "summary": "Input string is too long",
                            "value": {
                                "detail": [
                                    {
                                        "type": "string_too_long",
                                        "loc": ["body", "str_input"],
                                        "msg": "String should have be maximum 100,000 characters",
                                        "input": "",
                                        "ctx": {"max_length": 100000},
                                    }
                                ]
                            },
                        },
                        "str_input_too_short": {
                            "summary": "Input string is empty",
                            "value": {
                                "detail": [
                                    {
                                        "type": "string_too_short",
                                        "loc": ["body", "str_input"],
                                        "msg": "String should have at least 1 character",
                                        "input": "",
                                        "ctx": {"min_length": 1},
                                    }
                                ]
                            },
                        },
                        "missing_type": {
                            "summary": "Missing type query parameter",
                            "value": {
                                "detail": [
                                    {
                                        "type": "missing",
                                        "loc": ["query", "type"],
                                        "msg": "Field required",
                                        "input": None,
                                    }
                                ]
                            },
                        },
                        "unknown_type": {
                            "summary": "Unknown analyser type",
                            "value": {
                                "response": {},
                                "message": "Unknown analyser types: ['bad_type']",
                                "request_id": "abc-123",
                            },
                        },
                    }
                }
            },
        },
    },
)
async def analyses(
    response: Response,
    request: Request,
    str_input: StrInput,
    analysis_types: list[AnalysesTypes] = Query(
        ..., alias="type", description="One or more analyses types to run"
    ),
    api_key: str | None = Depends(get_model_api_key),
) -> AnalysisResponse:
    registry = request.app.state.registry
    request_id = request.state.request_id

    requested_types = [t.name for t in analysis_types]
    unknown_types = [
        analyser_type
        for analyser_type in requested_types
        if not registry.get(analyser_type)
    ]
    if unknown_types:
        logger.error("Unknown analyser types requested: {}", unknown_types)
        response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        return AnalysisResponse(
            response={},
            message=f"Unknown analyser types: {unknown_types}",
            request_id=request_id,
        )

    results: dict[str, str] = {}
    ctx = AnalysesContext(api_key=api_key)
    for analyser_type in requested_types:
        analyser = registry.get(analyser_type)
        result = await analyser.analyse(
            str_input=str_input,
            ctx=ctx,
        )
        results[analyser_type] = result

    response.status_code = status.HTTP_200_OK
    return AnalysisResponse(response=results, message="ok", request_id=request_id)
