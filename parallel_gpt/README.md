# Parallel GPT

이 프로젝트는 GPT 모델의 completion과 embedding 기능을 병렬로 처리하여, 분당 요청 처리량(RPM: Requests Per Minute)과 분당 토큰 처리량(TPM: Tokens Per Minute)을 최대한 효율적으로 사용할 수 있도록 구현한 코드입니다. Parallel GPT는 대규모 언어 모델을 사용하는 애플리케이션에서 필수적인 효율적인 자원 관리 및 활용을 가능하게 합니다. 이 코드를 통해 사용자는 GPT 모델의 병렬 처리 성능을 극대화하여, 동시에 다수의 요청을 빠르고 효율적으로 처리할 수 있습니다. 본 코드는 OpenAI의 Recipe를 참고하여 개발되었습니다.

## 사용 방법

본 코드의 자세한 사용 방법과 예시는 [`usage.ipynb`](./parallel_gpt/usage.ipynb) Jupyter 노트북에 정리되어 있습니다. 해당 노트북을 통해 각 기능의 구현 방법과 사용 예제를 확인할 수 있습니다.