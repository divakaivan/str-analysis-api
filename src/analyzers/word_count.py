from src.schemas import StrInput
from loguru import logger


class WordCountAnalyser:
    name = "word_count"

    async def analyse(self, str_input: StrInput, **kwargs) -> str:
        logger.info("calling word count analysis")
        return str(len(str_input.str_input.split()))
