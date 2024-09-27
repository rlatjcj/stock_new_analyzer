import os
from typing import List

from langchain_core.language_models.llms import BaseLLM
from langchain_openai import ChatOpenAI

OPENAI_MODELS = [
    "gpt-4-1106-preview",
    "gpt-4o-2024-05-13",
    "gpt-4-0125-preview",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo-16k",
    "gpt-4o-2024-08-06",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-instruct-0914",
    "gpt-4o",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo",
    "gpt-4-0613",
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-3.5-turbo-instruct",
    "gpt-3.5-turbo",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini"
]


def get_available_models() -> List[str]:
    return OPENAI_MODELS


def load_llm(model: str) -> BaseLLM:
    available_models = get_available_models()
    if model not in available_models:
        raise ValueError(
            f"모델 '{model}'은(는) 사용할 수 없습니다. "
            f"사용 가능한 모델: {', '.join(available_models)}")

    if model.startswith("gpt"):
        return ChatOpenAI(model=model, openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError(f"지원되지 않는 모델 유형입니다: {model}")
