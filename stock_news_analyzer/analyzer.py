from typing import Any, Dict, List

import bs4
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.language_models.llms import BaseLLM

from stock_news_analyzer.utils.logger import get_logger

logger = get_logger(__name__)


async def fetch_news_content(news_links: List[Dict[str, Any]]) -> List[str]:
    contents = []
    for news in news_links:
        try:
            loader = WebBaseLoader(
                web_path=news['link'],
                bs_kwargs=dict(
                    parse_only=bs4.SoupStrainer(
                        "div",
                        attrs={"class": ["newsct_article _article_body", "media_end_head_title"]},
                    )
                ),
            )
            docs = loader.load()
            contents.append(docs[0].page_content)
        except Exception as e:
            logger.error(f"뉴스 내용 가져오기 중 오류 발생: {e}")
    return contents


async def summarize_news(news_contents: List[str], llm: BaseLLM) -> str:
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.create_documents(news_contents)

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        combine_prompt=PromptTemplate(
            template="""아래와 같이 간결한 요약을 작성해줘:


                "{text}"


                간결한 요약:""",
            input_variables=["text"]
        )
    )
    summary = chain.invoke(split_docs)
    return summary


def analyze_sentiment(summary: str, company: str, llm: BaseLLM) -> str:
    sentiment_prompt = PromptTemplate(
        input_variables=["company", "summary"],
        template="다음은 {company}에 관한 여러 뉴스의 종합 요약입니다:\n\n{summary}\n\n"
                 "이 요약을 바탕으로 {company}에 대한 전반적인 뉴스 논조가 긍정적인지, 부정적인지, "
                 "중립적인지 판단하고, 그 이유를 간단히 설명해주세요. 또한, 가장 중요해 보이는 "
                 "3가지 핵심 포인트를 추출하여 나열해주세요."
    )

    try:
        sentiment_analysis = llm.invoke(sentiment_prompt.format(company=company, summary=summary))
        return sentiment_analysis
    except Exception as e:
        logger.error(f"감정 분석 중 오류 발생: {e}")
        return "감정 분석 실패"


async def analyze_news(
    news_links: List[Dict[str, Any]],
    company: str,
    llm: BaseLLM
) -> Dict[str, Any]:
    logger.info("뉴스 내용 가져오기 시작...")
    news_contents = await fetch_news_content(news_links)

    logger.info("뉴스 요약 시작...")
    summary = await summarize_news(news_contents, llm)

    logger.info("감정 분석 시작...")
    sentiment_analysis = analyze_sentiment(summary, company, llm)

    return {
        "summary": summary,
        "sentiment_analysis": sentiment_analysis
    }
