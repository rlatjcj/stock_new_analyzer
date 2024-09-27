<div align="center">

# Stock news analyzer

주식 뉴스 분석기는 [langchain](https://www.langchain.com/)을 사용하여 주식 관련 뉴스를 수집, 요약 및 분석하는 도구입니다. 이 분석기는 주식에 대한 일일 정보를 확인하는 데 사용될 수 있으며, 투자 전략 추천 등으로 확장할 수 있습니다.

</div>

## Features

- **뉴스 및 공시 수집**: 다양한 소스에서 주식 관련 뉴스 및 공시를 자동으로 수집합니다.
- **요약 기능**: 수집된 뉴스 및 공시를 간결하게 요약하여 핵심 정보를 제공합니다.
- **감정 분석**: 뉴스 및 공시의 감정을 분석하여 긍정적, 부정적 또는 중립적인 경향을 파악합니다.
- **투자 전략 추천**: 분석된 정보를 바탕으로 사용자에게 맞춤형 투자 전략을 제안합니다.
- **데이터 시각화**: 주식 뉴스 및 공시와 관련된 데이터를 시각적으로 표현하여 이해를 돕습니다.

## Installation

```bash
pip install stock-news-analyzer
```

## Usage

```bash
stock-news-analyzer -c 005930 -f 2024.01.01 -t 2024.01.31 -m gpt-4o
```

## License

This project is licensed under the Apache License 2.0.
