# Parallel GPT

OpenAI GPT API의 completion과 embedding 기능을 병렬로 처리하여, 분당 요청 처리량(RPM: Requests Per Minute)과 분당 토큰 처리량(TPM: Tokens Per Minute)을 최대한 효율적으로 사용할 수 있도록 구현한 코드입니다. 이 코드를 통해 OpenAI GPT API 병렬 처리 성능을 극대화하여, 동시에 다수의 요청을 빠르고 효율적으로 처리할 수 있습니다. 본 코드는 OpenAI의 Recipe를 참고하여 개발되었습니다.

## 사용 방법

본 코드의 자세한 사용 방법과 예시는 [`usage.ipynb`](https://github.com/jki0113/Cutsom-Utils/blob/main/parallel_gpt/usage.ipynbb) Jupyter 노트북에 정리되어 있습니다. 해당 노트북을 통해 각 기능의 구현 방법과 사용 예제를 확인할 수 있습니다.