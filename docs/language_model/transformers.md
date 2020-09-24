---
layout: default
title: Transformers
parent: Language Model
nav_order: 2
has_children: true
has_toc: false
---

# 트랜스포머(Transformer)
{: .no_toc }

트랜스포머(transformer)는 2017년 구글이 제안한 시퀀스-투-시퀀스(sequence-to-sequence) 모델입니다. 최근 자연어 처리에서는 BERT나 GPT 같은 트랜스포머 기반 언어모델이 각광받고 있습니다. 그 성능이 좋기 때문인데요. 왜 성능이 좋은지, 핵심 동작 원리는 무엇인지 이 글에서 살펴보겠습니다.
{: .fs-4 .ls-1 .code-example }

## Table of contents
{: .no_toc .text-delta .mt-6}

1. TOC
{:toc}

---

## 트랜스포머란?

트랜스포머(Transformer)란 기계 번역(machine translation) 등 시퀀스-투-시퀀스(sequence-to-sequence) 과제를 수행하기 위한 모델입니다. 여기에서 시퀀스란 단어(word) 같은 **무언가(something)의 나열**을 의미하는데요. '시퀀스-투-시퀀스'는 특정 속성을 지닌 시퀀스를 다른 속성의 시퀀스로 변환하는 작업을 가리킵니다.

기계 번역을 예시로 '시퀀스-투-시퀀스'가 어떤 태스크인지 알아봅시다. 기계 번역이란 어떤 언어(소스 언어, source language)의 문장을 다른 언어(대상 언어, target language)의 문장으로 변환하는 과제입니다. 그림1과 그림2에서는 소스 언어와 번역 대상 문장 각각에 형태소 분석을 실시한 결과를 나타내고 있습니다.

## **그림1** 소스 언어의 문장과 그 시퀀스
{: .no_toc .text-delta }
```
어제 카페 갔었어 거기 사람 많더라 > 어제, 카페, 갔었어, 거기, 사람, 많더라
```

## **그림2** 대상 언어의 문장과 그 시퀀스
{: .no_toc .text-delta }
```
i went to the cafe there were many people there > i, went, to, the, cafe, there, were, many, people, there
```

기계 번역에서 '시퀀스-투-시퀀스'란 **소스 언어의 단어 시퀀스**를 **대상 언어의 단어 시퀀스**로 변환하는 작업입니다. 그림3과 같습니다. 자세히 살펴보면 소스의 시퀀스 길이(단어 6개)와 대상 시퀀스의 길이(10개)가 다르다는 점을 알 수 있습니다. 이처럼 '시퀀스-투-시퀀스' 태스크는 소스와 대상의 길이가 달라도 해당 과제를 수행하는 데 문제가 없어야 합니다.

## **그림3** 기계 번역에서의 '시퀀스-투-시퀀스'
{: .no_toc .text-delta }
```
어제, 카페, 갔었어, 거기, 사람, 많더라 > i, went, to, the, cafe, there, were, many, people, there
```

트랜스포머는 이러한 '시퀀스-투-시퀀스' 과제 수행에 특화된 모델입니다. 임의의 시퀀스를 해당 시퀀스와 속성이 다른 시퀀스로 변환하는 작업이라면 꼭 기계 번역이 아니더라도 수행이 가능합니다. 예컨대 필리핀 앞바다의 한 달치 기온 데이터를 가지고 앞으로 1주일간 태풍이 발생할지 여부를 맞추는 과제(기온의 시퀀스 > 태풍 발생 여부의 시퀀스) 역시 트랜스포머가 할 수 있는 일입니다.

'시퀀스-투-시퀀스' 과제를 수행하는 모델은 대개 인코더(encoder)와 디코더(decoder) 두 개 파트로 구성되어 있습니다(그림4). 인코더는 소스 시퀀스의 정보를 압축해 디코더로 보내주는 역할을 담당합니다. 인코더가 소스 시퀀스 정보를 압축하는 과정을 인코딩(encoding)이라고 합니다.

디코더는 인코더가 보내준 소스 시퀀스 정보를 받아서 대상 시퀀스를 생성하게 됩니다. 디코더가 대상 시퀀스를 생성하는 과정을 디코딩(decoding)이라고 합니다. 기계번역 예시에서는 인코더가 한국어 문장을 압축해 디코더에 보내고, 디코더는 이를 받아 영어로 번역합니다.

## **그림4** 인코더, 디코더
{: .no_toc .text-delta }
<img src="https://i.imgur.com/l0RJkOv.png" width="300px" title="source: imgur.com" />

여기에서 디코더 입력을 좀 더 자세히 살펴볼 필요가 있습니다. 그림5를 봅시다. 디코더는 디코딩을 수행할 때 우선 인코더가 보내준 소스 시퀀스 정보를 활용합니다. **여기에 직전 디코딩 결과도 씁니다.** 그림5 예시에서 디코더가 대상 언어의 세번째 자리를 예측해야 할 때 `어제, 카페, 갔었어, 거기, 사람, 많더라`라는 소스 언어의 인코딩 결과뿐 아니라 직전 `I, went`라는 직전 디코딩 결과까지도 활용한다는 것입니다.

## **그림5** 디코더 입력 (그림5는 트랜스포머와 글 전체 예시에 맞게 그림을 고쳐야 함)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/wgMefCX.png" width="300px" title="source: imgur.com" />

그럼 여기에서 하나 의문이 생길 수 있습니다. 직전 디코딩 결과가 완전히 틀렸다면 이후 디코딩 결과를 신뢰할 수 있는 걸까요? 그림5처럼 첫 단어의 정답은 `I`인데 이를 `You`로 예측했다면 이후 디코딩 결과는 정답과 거리가 멀 가능성이 꽤 높습니다. 디코더는 직전 디코딩 결과를 디코딩에 적극 활용하기 때문입니다. 이 때문에 **학습 과정에서는 직전 디코딩 결과가 무엇이 됐든 무시하고 현재 디코더 입력에 정답을 넣어줍니다.** 그림6과 같습니다.

## **그림6** 학습 과정에서의 디코더 입력 (그림6은 트랜스포머와 글 전체 예시에 맞게 그림을 고쳐야 함)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/wgMefCX.png" width="300px" title="source: imgur.com" />

트랜스포머 역시 인코더와 디코더 구조를 따르고 있습니다. 그림7과 같습니다. 그림7 왼편이 인코더이고 오른편이 디코더입니다. 인코더의 입력(그림에서 `Inputs`)은 소스 시퀀스입니다. 디코더의 입력(그림7에서 `Outputs`)은 대상 시퀀스의 일부입니다. 

예컨대 이번 학습은 대상 언어의 3번째 단어(`to`)를 맞춰야 하는 차례라고 가정해 봅시다. 이 경우 인코더 입력은 `어제, 카페, 갔었어, 거기, 사람, 많더라` 같이 소스 시퀀스 전체가 되고 디코더 입력은 대상 시퀀스 전체(`i, went, ..., there` 총 10개 단어) 가운데 앞부분인 `GO, I, went`가 됩니다. 

이번 학습이 대상 언어의 4번째 단어(`the`)를 맞춰야 하는 차례일 때 인코더 입력은 소스 시퀀스 전체, 디코더 입력은 `GO, I, went, to`가 됩니다. 인코더, 디코더 입력은 [모델 입력과 출력](https://ratsgo.github.io/nlpbook/docs/language_model/transformers/#%EB%AA%A8%EB%8D%B8-%EC%9E%85%EB%A0%A5%EA%B3%BC-%EC%B6%9C%EB%A0%A5)에서 좀 더 자세히 살펴보겠습니다.

## **그림7** Transformer
{: .no_toc .text-delta }
<img src="https://i.imgur.com/Rk5wkBQ.png" width="400px" title="source: imgur.com" />
<img src="https://i.imgur.com/F0qY4ny.png" width="400px" title="source: imgur.com" />

트랜스포머의 최종 출력, 즉 디코더 출력(그림7에서 `Output Probabilities`)은 소스 언어의 어휘 수만큼의 차원을 갖는 확률 벡터(random vector)가 됩니다. 확률 벡터란 요소(element) 값이 모두 확률인 벡터를 의미하는데요. 

소스 언어의 어휘가 총 3만개라고 가정해봅시다. 그렇다면 디코더 출력은 3만 차원의 확률 벡터입니다. 이 벡터의 요소 값 3만개는 모두 확률이므로 3만개 요소값을 다 더하면 그 합은 1이 됩니다. **트랜스포머의 학습은 인코더와 디코더 입력이 주어졌을 때 정답에 해당하는 단어의 확률 값을 높이는 방식으로 수행**됩니다. 

이와 관련해 그림8 예시를 봅시다. 예시에서는 대상 언어의 3번째 단어(`to`)를 맞춰야 하는 차례입니다. 인코더 입력은 `어제, 카페, 갔었어, 거기, 사람, 많더라` 같이 소스 시퀀스 전체가 되고 디코더 입력은 대상 시퀀스 전체(`i, went, ..., there` 총 10개 단어) 가운데 앞부분인 `GO, I, went`가 됩니다. 

이로부터 트랜스포머 모델은 이번 시점의 정답인 `to`에 해당하는 확률은 높이고 나머지 단어의 확률은 낮아지도록, 모델 전체를 업데이트합니다. 이를 학습(train)이라고 합니다. 이렇게 학습 데이터 말뭉치(corpus) 전체를 학습하게 되면 소스 언어에서 대상 언어로 변환하는 기계 번역 태스크를 성공적으로 수행할 수 있게 됩니다.

## **그림8** 디코더 출력 (Output probabilities)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/Kd1TIRo.jpg" width="800px" title="source: imgur.com" />

그림9는 트랜스포머의 인코더 가운데 반복되는 요소를 떼어내 다시 그린 것입니다. 그림9 같은 구조를 블록(block) 혹은 레이어(layer)라고 부릅니다. 트랜스포머의 인코더는 이같은 블록을 6\~24개를 쌓아서 구성합니다. 디코더 쪽 블록의 구조도 그림9의 인코더 블록과 본질적으로는 다르지 않습니다. 

## **그림9** 트랜스포머 인코더 블록
{: .no_toc .text-delta }
<img src="https://i.imgur.com/NSmVlit.png" width="150px" title="source: imgur.com" />

그림9에 도시된 블록은 트랜스포머의 핵심에 해당합니다. 트랜스포머 경쟁력의 원천은 이 블록에 있다고 해도 과언이 아닐 정도죠. 이 블록의 구성 요소는 ∆ 멀티-헤드 어텐션(Multi-Head Attention) ∆ 피드포워드 뉴럴네트워크(Feedforward Neural Network) ∆ Add & Norm 등 세 가지입니다. 이후 장에서 차례대로 살펴보겠습니다.


---

## 셀프 어텐션


그림9 트랜스포머 인코더 블록의 멀티-헤드 어텐션은 **셀프 어텐션(self attention)**이라는 기법을 여러 번 수행한 걸 가리킵니다. 하나의 헤드(head)가 셀프 어텐션을 1회 수행하고 이를 여러 개 헤드가 독자적으로 각각 계산한다는 이야기라는 말입니다.

어텐션(attention)은 시퀀스 입력에 수행하는 기계학습 방법의 일종인데요. **어텐션은 시퀀스 요소들 가운데 태스크 수행에 중요한 요소에 집중하고 그렇지 않은 요소는 무시해 태스크 수행 성능을 끌어 올립니다.** 어텐션은 기계 번역 과제에 처음 도입됐습니다.

기계 번역에 어텐션을 도입한다면 대상 언어를 디코딩할 때 소스 언어의 단어들(시퀀스) 가운데 디코딩에 도움되는 단어들 위주로 취사 선택해 번역 품질을 끌어 올리게 됩니다. 요컨대 어텐션은 대상 시퀀스(target sequence) 디코딩시 소스 시퀀스(source sequence)를 참조해 소스 시퀀스 가운데 중요한 요소들만 추립니다.

셀프 어텐션이란 말 그대로 자기 자신에 수행하는 어텐션 기법입니다. 입력 시퀀스 가운데 태스크 수행에 의미 있는 녀석들 위주로 정보를 추출한다는 것이죠.

이렇게만 설명한다면 너무 알쏭달쏭하니 자연어 처리에서 자주 쓰이는 리커런트 뉴럴네트워크(Recurrenct Neural Network, RNN), 컨볼루션 뉴럴네트워크(Convolutional Neural Network, CNN) 등과 비교를 통해 셀프 어텐션이 대체 어떤 점을 목표로 하는지 자세히 살펴보도록 하겠습니다.

CNN은 시퀀스의 지역적인 특징을 잡아내는 데 유리한 모델입니다. 자연어는 기본적으로 시퀀스(단어 혹은 형태소의 나열)이고 특정 단어 기준 주변 문맥이 의미 형성에 중요한 역할을 하기 때문에 CNN은 자연어 처리에 널리 쓰이고 있습니다. 

그림10은 CNN이 문장을 어떻게 인코딩하는지 도식적으로 나타낸 것입니다. 컨볼루션 필터(그림10에서 붉은색 네모칸)이 단어를 하나씩 슬라이딩하면서 차례대로 읽어들이는 걸 알 수 있습니다.

하지만 CNN은 컨볼루션 필터 크기를 넘어서는 문맥은 읽어내기 어렵다는 단점이 있습니다. 예컨대 필터 크기가 3(3개 단어 처리)이라면 5칸 이상 떨어져 있는 단어 사이의 의미는 캐치하기 어렵다는 것입니다.

## **그림10** 컨볼루션 뉴럴 네트워크(Convolutional Neural Network)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/3pn5n0C.png" width="500px" title="source: imgur.com" />
<br>
<img src="https://i.imgur.com/tk2s2eR.png" width="500px" title="source: imgur.com" />
<br>
<img src="https://i.imgur.com/QZ7QV6v.png" width="500px" title="source: imgur.com" />

RNN 역시 시퀀스 정보를 압축하는 데 강점이 있는 구조입니다. 소스 언어 시퀀스, `어제, 카페, 갔었어, 거기, 사람, 많더라`를 인코딩해야 한다고 가정해 봅시다. 그렇다면 RNN은 그림11과 같이 소스 시퀀스를 순차적으로 처리하게 됩니다.

하지만 RNN은 시퀀스 길이가 길어질 수록 정보 압축에 문제가 생기게 됩니다. 오래 전에 입력된 단어는 잊어버리거나, 특정 단어 정보를 과도하게 반영해 전체 정보를 왜곡하는 경우가 자주 생긴다는 것입니다.

## **그림11** 리커런트 뉴럴 네트워크(Recurrenct Neural Network)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/5eAs55K.png" width="500px" title="source: imgur.com" />

기계 번역시 소스 언어의 문장을 인코딩할 때 RNN을 사용했다고 칩시다. 이 경우 인코더가 디코더로 넘기는 정보는 소스 시퀀스의 마지막인 `많더라`라는 단어의 의미가 많이 반영될 수밖에 없습니다. RNN은 입력 정보를 순차적으로 처리하기 때문입니다.

그림12를 보면 `cafe`에 대응하는 소스 언어의 단어는 `카페`이고 이는 소스 시퀀스의 초반부에 등장한 상황입니다. `cafe`라는 단어를 디코딩해야 하는 경우 `카페`를 반드시 참조해야 하는데요. 단순 RNN을 사용하면 워낙 오래 전에 입력된 단어라 모델이 잊었을 가능성이 높고 이 때문에 번역 품질이 낮아질 수 있습니다.

어텐션은 RNN의 이러한 문제점을 해결하기 위해 제안된 기법입니다. 어텐션은 대상 언어 디코딩시 소스 시퀀스 전체에서 어떤 요소에 주목해야 할지 알려주기 때문에 `카페`가 시퀀스 초반에 등장하더라도, 소스 시퀀스의 길이가 길어지더라도 번역 품질 하락을 막을 수 있게 됩니다. 그림12의 예시에서는 주목해야 할 단어에 좀 더 짙고 굵은 실선을 그려 놓았습니다.

## **그림12** 기존 어텐션(Sequence-to-Sequence Attention)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/kRjEkPm.png" width="500px" title="source: imgur.com" />

셀프 어텐션은 자기 자신에 수행하는 어텐션입니다. 그림13을 봅시다. 입력 시퀀스가 `어제, 카페, 갔었어, 거기, 사람, 많더라`일 때 `거기`라는 단어가 어떤 의미를 가지는지 계산하는 상황입니다. 

잘 학습된 셀프 어텐션 모델이라면 `거기`에 대응하는 장소는 `카페`라는 사실을 알아챌 수 있을 것입니다. 뿐만 아니라 `거기`는 `갔었어`와도 연관되어 있음을 확인할 수 있습니다. 트랜스포머 인코더 블록 내부에서는 이처럼 `거기`라는 단어를 인코딩할 때 `카페`, `갔었어`라는 단어의 의미를 강조해 반영합니다.

## **그림13** 셀프 어텐션(Self Attention) (1)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/l7JogVh.png" width="500px" title="source: imgur.com" />

그림14는 입력 시퀀스가 입력 시퀀스가 `어제, 카페, 갔었어, 거기, 사람, 많더라`일 때 `카페`라는 단어가 어떤 의미를 가지는지 계산하는 상황입니다. 트랜스포머 인코더 블록은 `카페`라는 단어를 인코딩할 때 `거기`, `갔었어`라는 단어의 의미를 다른 단어들보다 더 강하게 반영합니다.

## **그림14** 셀프 어텐션(Self Attention) (2)
{: .no_toc .text-delta }
<img src="https://i.imgur.com/YUcm8xS.png" width="500px" title="source: imgur.com" />

셀프 어텐션 수행 대상은 입력 시퀀스 전체입니다. `거기`(그림13)와 `카페`(그림14)만을 예로 들었지만 실제로는 `어제`-전체 입력 시퀀스, `갔었어`-전체 입력 시퀀스, `사람`-전체 입력 시퀀스, `많더라`-전체 입력 시퀀스 모두 어텐션 계산을 합니다. 

개별 단어와 전체 입력 시퀀스를 대상으로 어텐션 계산을 수행해 문맥 전체를 고려하기 때문에 지역적인 문맥만 보는 CNN 대비 강점이 있습니다. 아울러 단어들 서로가 서로를 1대 1로 바라보기 때문에 시퀀스 길이가 길어지더라도 정보를 잊거나 왜곡할 염려가 없습니다. 이는 RNN의 단점을 극복한 지점입니다.


한편 어텐션과 셀프 어텐션이 다른 지점이 있다면 기존 어텐션은 RNN 구조를 보정하기 위해 제안된 아키텍처라면, 셀프 어텐션은 RNN을 제거하고 아예 어텐션으로만 인코더 디코더 구조를 만들었다는 점이 다릅니다.
{: .fs-4 .ls-1 .code-example }


++ BERT & GPT 설명할 때 쿼리, 키, 밸류 활용하므로 셀프 어텐션 계산 예시를 여기에 넣자

---


## 참고 문헌

- [Illustrated: Self-Attention](https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a)


---