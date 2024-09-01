import bs4
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader


def main():
    loader = WebBaseLoader(
        web_paths=("https://n.news.naver.com/article/437/0000378416",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                "div",
                attrs={"class": ["newsct_article _article_body", "media_end_head_title"]},
            )
        ),
    )

    docs = loader.load()
    print(f"문서의 수: {len(docs)}")
    print(docs)


if __name__ == "__main__":
    load_dotenv()
    main()
