---
layout: default
title: Paper Book Notice
nav_order: 10
has_children: false
has_toc: false
permalink: /docs/notice
---

# 종이책 정오표
{: .no_toc }

종이책 오탈자 및 수정 사항을 안내합니다. 해당 내용은 [nlpbook issue](https://github.com/ratsgo/nlpbook/issues)에서 토론을 거쳐 확정된 것입니다. 여기에 나오지 않는 사항이라도 언제든지 편하게 리포트 해주세요! 정정 의견은 [github.com](https://github.com)에 회원 가입을 한 뒤 [nlpbook issue 등록 항목](https://github.com/ratsgo/nlpbook/issues/new)에서 제목과 본문을 입력하면 등록할 수 있습니다.
{: .fs-4 .ls-1 .code-example }

## Table of contents
{: .no_toc .text-delta .mt-6}

1. TOC
{:toc}

---

## 54페이지

다음 문단을 교체.

**수정 전**

> 한글은 한 글자가 3개의 유니코드 바이트로 표현되는데요, 예를 들어 안녕하세요라는 문자열을 유니코드 바이트로 변환하면 다음처럼 됩니다. 안녕하세요 → ìķĪëħķíķĺìĦ ̧ìļĶ

> 바이트 수준으로 BPE를 수행한다는 것은 어휘 집합 구축 대상 말뭉치를 위와 같이 모두 유니 코드 바이트로 변환하고 이들을 문자 취급해 가장 자주 등장한 문자열을 병합하는 방식으로 어휘 집합을 만든다는 의미입니다. 토큰화 역시 문자열을 유니코드 바이트로 일단 변환한 뒤 수행합니다.

**수정 후**

> 한글은 한 글자가 3개의 유니코드 바이트로 표현되는데요, 예를 들어 안녕하세요라는 문자열을 각각의 유니코드 바이트에 대응하는 문자\*로 변환하면 다음처럼 됩니다. 안녕하세요 → ìķĪëħķíķĺìĦ ̧ìļĶ

> \* 유니코드(UTF-8) 1바이트를 10진수로 표현하면 0에서 255 사이의 정수가 됩니다. 이 256개 정수 각각을 특정 문자로 매핑한 것입니다. 예컨대 0은 Ā, 255는 ÿ에 각각 대응합니다.

> 바이트 수준으로 BPE를 수행한다는 것은 어휘 집합 구축 대상 말뭉치를 위와 같이 변환하고 이들을 문자 취급해 가장 자주 등장한 문자열을 병합하는 방식으로 어휘 집합을 만든다는 의미입니다. 토큰화 역시 원래 문자열을 위와 같이 변환한 뒤 수행합니다.

---

## 237페이지

다음 문단을 교체.

**수정 전**

> 샘플링 방식 예를 든 다음 그림을 보면 그라는 컨텍스트를 입력했을 때 모델은 다음 토큰으로 집(0.5), 책(0.4), 사람(0.1)이 그럴듯하다고 예측했습니다. 여기에서 다음 토큰을 확률적으로 선택합니다. 집이 선택될 가능성이 50%로 제일 크고 사람이 선택될 가능성도 10%로 작지만 없지 않습니다.

**수정 후**

> 샘플링 방식 예를 든 다음 그림을 보면 그라는 컨텍스트를 입력했을 때 모델은 다음 토큰으로 책(0.5), 집(0.4), 사람(0.1)이 그럴듯하다고 예측했습니다. 여기에서 다음 토큰을 확률적으로 선택합니다. 책이 선택될 가능성이 50%로 제일 크고 사람이 선택될 가능성도 10%로 작지만 없지 않습니다.


그림 8-8을 다음으로 교체.

<img width="500" src="https://user-images.githubusercontent.com/26211652/147377581-e8abb8d9-6db6-4a0b-aa37-d7e6497db2a7.png">

---

## 240페이지


그림 8-11을 다음으로 교체.

<img width="500" src="https://user-images.githubusercontent.com/26211652/147377570-42915486-d087-49f3-8834-2d579654d5ee.png">


---