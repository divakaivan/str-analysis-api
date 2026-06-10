from fastapi import HTTPException, status
from loguru import logger

from src.schemas import StrInput, AnalysesContext


class SemanticAnalyser:
    name = "semantic"

    async def analyse(self, str_input: StrInput, ctx: AnalysesContext) -> str:
        logger.info("calling semantic analysis")
        api_key = ctx.api_key

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required for semantic analysis",
            )

        # result = await modernBERT(str_input)
        result = f"'{str_input.str_input}' is fine"
        logger.info("semantic analysis produced result")
        return result
