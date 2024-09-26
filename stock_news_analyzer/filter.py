from typing import Any, Dict, List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.language_models.llms import BaseLLM

# flake8: noqa


def create_similarity_chain(llm: BaseLLM) -> LLMChain:
    similarity_template = """
    다음 두 뉴스 제목이 같은 내용을 다루고 있는지 판단해주세요:

    제목 1: {title1}
    제목 2: {title2}

    만약 두 제목이 같은 내용을 다루고 있다면 "유사"라고 답변하고, 그렇지 않다면 "다름"이라고 답변해주세요.

    답변:
    """

    similarity_prompt = PromptTemplate(
        input_variables=["title1", "title2"],
        template=similarity_template
    )

    return LLMChain(llm=llm, prompt=similarity_prompt)

def filter_similar_news(news_list: List[Dict[str, Any]], llm: BaseLLM) -> List[Dict[str, Any]]:
    similarity_chain = create_similarity_chain(llm)
    filtered_news: List[Dict[str, Any]] = []
    for news in news_list:
        is_similar = False
        for filtered in filtered_news:
            response = similarity_chain.run(title1=news['title'], title2=filtered['title'])
            if response.strip().lower() == "유사":
                is_similar = True
                break
        if not is_similar:
            filtered_news.append(news)
    return filtered_news
