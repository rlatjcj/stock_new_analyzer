<div align="center">

# Stock news analyzer

Stock news analyzer는 [langchain](https://www.langchain.com/)을 사용하여 주식 관련 뉴스를 수집, 요약 및 분석하는 도구입니다. 이 분석기는 주식에 대한 일일 정보를 확인하는 데 사용될 수 있으며, 투자 전략 추천 등으로 확장할 수 있습니다.

</div>

## Features

- **뉴스 및 공시 수집**: 다양한 소스에서 주식 관련 뉴스 및 공시를 자동으로 수집합니다.
- **요약 기능**: 수집된 뉴스 및 공시를 간결하게 요약하여 핵심 정보를 제공합니다.
- **감정 분석**: 뉴스 및 공시의 감정을 분석하여 긍정적, 부정적 또는 중립적인 경향을 파악합니다.
- [TODO] **투자 전략 추천**: 분석된 정보를 바탕으로 사용자에게 맞춤형 투자 전략을 제안합니다.
- [TODO] **데이터 시각화**: 주식 뉴스 및 공시와 관련된 데이터를 시각적으로 표현하여 이해를 돕습니다.

## Installation

```bash
pip install stock-news-analyzer
```

## Usage

```bash
$ stock-news-analyzer -c SK하이닉스   -f 2024.09.27 -t 2024.09.27 -p 1 -m gpt-4o-mini

USER_AGENT environment variable not set, consider setting it to identify your requests.
2024-09-28 01:27:06,414 - stock_news_analyzer.finder - INFO - 뉴스 검색 시작: 회사 - SK하이닉스, 기간 - 2024.09.27 ~ 2024.09.27
2024-09-28 01:27:06,597 - stock_news_analyzer.finder - INFO - 총 9개의 뉴스를 찾았습니다.
2024-09-28 01:27:06,597 - stock_news_analyzer.finder - INFO - [2024.09.27 22:43] 반도체 핵심기술 중국 유출…전 삼성전자 임원 등 2명 구속기소동영상기사 - https://n.news.naver.com/mnews/article/422/0000684357
2024-09-28 01:27:06,597 - stock_news_analyzer.finder - INFO - [2024.09.27 20:55] 반도체株 롤러코스터에 질린 개미들…목표가 쭉쭉 오르는 ‘이 종목’ 찾는... - https://n.news.naver.com/mnews/article/009/0005371516
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 19:01] 대한전자공학회 "온디바이스 AI용 반도체 집중 육성해야" - https://n.news.naver.com/mnews/article/092/0002346951
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 18:26] 올해도 '묻지마 증인채택'…과방위 역대 최대 161명 줄소환 - https://n.news.naver.com/mnews/article/011/0004397091
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 18:03] "반도체 겨울 틀렸다" 모건스탠리 굴욕 - https://n.news.naver.com/mnews/article/009/0005371476
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 17:52] 하이닉스 사는 외국인, 삼성전자는 내다 판다 - https://n.news.naver.com/mnews/article/015/0005038051
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 17:48] 美·日 보조금 퍼붓는데…K반도체 R&D '세계 최하위' - https://n.news.naver.com/mnews/article/011/0004397066
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 17:42] Value-up index gets dressing down from ... - https://n.news.naver.com/mnews/article/640/0000059449
2024-09-28 01:27:06,598 - stock_news_analyzer.finder - INFO - [2024.09.27 17:39] 한화인더스트리얼솔루션즈 재상장…3남 김동선 합류 - https://n.news.naver.com/mnews/article/215/0001181402
2024-09-28 01:27:06,711 - stock_news_analyzer.analyzer - INFO - 뉴스 내용 가져오기 시작...
2024-09-28 01:27:15,600 - stock_news_analyzer.analyzer - INFO - 뉴스 요약 시작...
2024-09-28 01:27:56,033 - stock_news_analyzer.analyzer - INFO - 감정 분석 시작...
2024-09-28 01:27:59,610 - stock_news_analyzer.cli - INFO - 분석 결과:
2024-09-28 01:27:59,610 - stock_news_analyzer.cli - INFO - 요약: 두 전 삼성전자 임원이 중국에 회사를 설립하기 위해 핵심 반도체 기술을 도용한 혐의로 체포 및 기소되었다. 투자자들은 반도체 주식에 대한 관심을 높이고 있으며, 삼성전자의 주가 변동에 따라 포트폴리오 다각화를 권장받고 있다. Yuhan Corporation은 FDA 승인을 받은 신약으로 성장 중이며, Cosmax Korea는 고수익 제품으로 주목받고 있다.

10월 26일, 'AIoT 기술 및 비즈니스 포럼'이 개최되어 온디바이스 AI의 중요성을 강조하였다. 한국의 반도체 산업은 R&D 지출이 낮아 경쟁력에 위협을 받고 있으며, 정부의 지원이 시급하다는 경고가 나왔다.

한국 가치 상승 지수는 구성 주식 선정 기준에 대한 비판을 받고 있으며, KRX는 지수 개편을 고려 중이다. 한화 산업 솔루션은 글로벌 반도체 장비 시장 진출을 목표로 새롭게 출범하였다.
2024-09-28 01:27:59,610 - stock_news_analyzer.cli - INFO - 감정 분석 및 핵심 포인트: 전반적인 뉴스 논조는 **중립적**이라고 판단됩니다. SK하이닉스에 대한 뉴스는 긍정적인 요소와 부정적인 요소가 혼재되어 있으며, 특히 반도체 시장의 불확실성과 관련된 우려가 강조되고 있지만 동시에 회사의 성장 가능성에 대한 기대감도 존재합니다.

### 핵심 포인트:
1. **기술 유출 사건**: 전 삼성전자 임원이 중국에 반도체 기술을 유출한 사건이 보도되며, 이는 반도체 산업의 신뢰성에 부정적인 영향을 미칠 수 있음.

2. **투자자 관점**: SK하이닉스의 주가는 외국인 투자자들의 대규모 매수로 상승세를 보이고 있으며, 이는 반도체 시장 내 고대역폭 메모리(HBM)의 성장 가능성에 대한 긍정적인 기대감을 나타냄.

3. **R&D 투자 부족**: 한국 반도체 산업이 전세계에서 R&D 투자 비중이 낮아 경쟁력이 위협받고 있으며, 이에 대한 정부의 지원 필요성이 강조되고 있음.

```

## License

This project is licensed under the Apache License 2.0.
