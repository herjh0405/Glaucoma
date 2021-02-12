# 🏥 Glaucoma prediction using AI

부산대학교 산업수학센터 `박정례` 박사님 지도 아래서 연구 수행 중 (2021.01.06 ~ )

---

## 개요

녹내장은 시신경 손상에 의해 발생된 시야결손이 진행되어 결국 실명에 이르는 안과 질환이다. 손상된 시신경의 재생 치료방법이 부재하므로 여러 머신러닝 기법들을 이용하여 손상전에 진단하여 예방하고자 함.

- (1995) Modelling series of visual fields to detect progression in normal-tension glaucoma
  - 곡선 적합 모델을 비교, 미래의 시각장 상태를 예측할 수 있는 가능성이 있음(?)
- (2012) Visual Field Progression in Glaucoma: Estimating the Overall Significance of Deterioration with Permutation Analyses of Pointwise Linear Regression (PoPLR)
  - linear regression 모델이 미래의 시각장 예측에 적합함을 보임
- (2011) A method to measure and predict rates of regional visual field decay in glaucoma
  - linear, quadratic, and exponential 모델들을 비교, exponential 모델이 가장 적합
- (2014) A new approach to measure visual field progression in glaucoma patients using variational Bayes linear regression
  - 머신러닝 알고리즘의 일종인 variational Bayes linear regression(VBLR)을 사용, 우수한 성능을 입증했다고 보고
- (2019) Visual Field prediction using Recurrent Neural Network**(Park, K., Kim, J., & Lee, J. *Scientific Reports*, *9*(1), 1–12.) [link](https://doi.org/10.1038/s41598-019-44852-6) 
  - 기존의 OLR 보다 RNN 이 성능이 더 좋음을 확인

위의 논문들을 참고하여 더 나은 모델을 만들어보고자 함.

---

## 데이터

* 부산소재지 ㄷ병원과 ㅂ병원의 현업 데이터
  *  데이터 유출의 위험 때문에 차트번호 -> 랜덤화, 생년월일 -> 검사 당시 연령, 이름 -> 삭제
* 환자의 차트번호, 나이, 눈, 검사날짜, THV, TDV 등의 시야검사 데이터로 이루어져 있음.

<img src = "https://user-images.githubusercontent.com/54921730/107731165-988e7080-6d38-11eb-9c38-f80e4a6ac902.png" width = 1000 max-width = 100% height = auto />

---

## 데이터 추가 설명

<img src = "https://user-images.githubusercontent.com/54921730/107731008-30d82580-6d38-11eb-8f80-8c2ad9993e4c.gif" width = 1000 max-width = 100% height = 600/>

거짓 양성, 거짓음성, 고정 손실 모두 33% 미만으로 정의되었다. 정상에 대해서는 GHT, MD, PSD가 정상 모집단의 95% 이내에 있는 대상으로 정의하였고, 녹내장은 GHT가 Outside Normal Limits 이거나 PSD가 95% 벗어난 경우로 정의하였다.(MD에 대한 언급은 없음)

>- False Positive : 번쩍하지 않았는데 버튼을 누른 경우 (실제 음성인데 양성으로 판정)
>
>- False Negative : 번쩍했는데 버튼을 누르지 않은 경우 (실제 양성인데 음성으로 판정)
>
>- Fixation Loss : 가운데를 얼마나 잘 보고있어나를 보여주는 지표
>
>  위의 수치들이 높으면 검사를 잘못한것
>
>- 반드시 검사를 두번 이상 진행해서 진행 과정을 확인 후 녹내장 진단
>- GHT
>  - Within normal limit : 위,아래 감도차이가 없는 정상적인 경우
>  - Borderline : 위,아래 시야의 감도차이가 약간 있는 초기 녹내장인 경우
>  - Outside normal limits : 위,아래 시야의 감도차이가 현저한 경우
>- VFI : 100%가 정상, 숫자가 적어질수록 감도가 낮아짐 
>
>- MD(Mean Deviation) : 음수값이 클수록 좋지 않음
>  - 초기 : MD > -6
>  - 중기 : -12 < MD < -6
>  - 말기 : MD < -12
>- PSD : 환자의 각 지점의 감도 패턴이 얼마나 불규칙적인지 나타내는 지표
>  - 수치가 클수록 좋지 않음 
>- P-value : 5% 이하로 나오면 좋지 않음 
>  - 3개 지점에서 p<0.05 이며, 3개중 하나는 p<0.01
>
>- 시야 악화 판단 방법
>  - 이전 검사에서 정상 영역이었으나, 새로운 결함으로 판단
>    - 3-point에서 각각 5dB씩 악화되고, 그 중 1-point가 10dB이 악화됨
>  - 이전 검사에서 이상 부위였으며,  더 악화된 것으로 판단
>    - 이전 3개의 이상 point 에서 각각 10dB씩 악화
>  - 악화 영역이 넓어지는 것으로 판단
>    - 2개 이상의 새로운 연속 지점이 포함됨
>
>https://blog.naver.com/seeyou_eye/221772316931

<img src = "https://user-images.githubusercontent.com/54921730/107731656-d5a73280-6d39-11eb-9c39-b701a7aecc45.png" width = 1000 max-width = 100% height = auto/>

> * THV : 피검사자가 반응한 가장 sensitive한 시표의 밝기
> * TDV : THV - 일반인들의 평균
> * PDV : TDV + Overall sensitivity changes
>   * TDV의 같은 값이라도 시야의 위치에 따라 다를 수 있음, 눈의 중심에 가까울 수록 중요

---

## 전처리

**Imports**

<img src = "https://user-images.githubusercontent.com/54921730/107732966-16ed1180-6d3d-11eb-9f99-f1d0346df8cc.png" width = 1000 max-width = 100% height = auto/>

**이상치 데이터**

* 같은 날 같은 눈을 2번 검사한 데이터가 있음
  * 검사결과가 이상할 경우 한번 더 검진해본다고 함,
    * 따라서 16일 이내에 같은 검사를 했을 경우 최신의 검진결과만 사용하기로 함.

<img src = "https://user-images.githubusercontent.com/54921730/107739052-56baf580-6d4b-11eb-8b35-8a268db8f16c.png" width = 1000 max-width = 100% height = auto/>

* 제거할 데이터의 인덱스를 뽑아내는 과정

<img src = "https://user-images.githubusercontent.com/54921730/107739167-a1d50880-6d4b-11eb-8616-7cc39df521fa.png" width = 1000 max-width = 100% height = auto/>

* 시계열 데이터이기에 검진횟수가 너무 적을 경우 의미가 없다고 판단
  * 최소 4회의 검진을 한 환자의 데이터만 사용하기로 결정
* 검진횟수가 적은 환자를 걸러내는 코드

<img src = "https://user-images.githubusercontent.com/54921730/107739459-45beb400-6d4c-11eb-8403-71dda1c61949.png" width = 1000 max-width = 100% height = auto/>

<img src = "https://user-images.githubusercontent.com/54921730/107739522-6850cd00-6d4c-11eb-9414-d8383ea1a220.png" width = 1000 max-width = 100% height = auto/>

## 시각화

* THV 값을 제외한 다른 값에서는 26, 35번 데이터가 제대로 측정이 안되는 것을 확인
  * 맹점이라 제대로 측정이 이루어지지 않음
* PDP, TDP는 P-value에 관한 것이므로 우선 PDV, THV, TDV를 먼저 살펴본다. 
  * 그 중에서도 THV를 우선적으로 살펴본다.

>* PDP
>
><img src = "https://user-images.githubusercontent.com/54921730/107739714-d7c6bc80-6d4c-11eb-9638-432a84e8e11f.png" width = 1000 max-width = 100% height =500/>
>
>* PDV : TDV + Overall sensitivity
>
><img src = "https://user-images.githubusercontent.com/54921730/107739892-46a41580-6d4d-11eb-9045-1726f03b093b.png" width = 1000 max-width = 100% height = auto/>
>
>* THV : 기계에서 환자가 반응한 가장 sensitive한 시표의 밝기
>
><img src = "https://user-images.githubusercontent.com/54921730/107739899-4b68c980-6d4d-11eb-8dbc-1dd8794c5344.png" width = 1000 max-width = 100% height = auto/>
>
>* TDP
>
><img src = "https://user-images.githubusercontent.com/54921730/107739905-4e63ba00-6d4d-11eb-87ae-154d6a7b96c6.png" width = 1000 max-width = 100% height = auto/>
>
>* TDV : THV - 일반인들의 평균
>
><img src = "https://user-images.githubusercontent.com/54921730/107739913-515eaa80-6d4d-11eb-9485-f01ee51bb54e.png" width = 1000 max-width = 100% height = auto/>

---

## 두 번째 전처리 

**이상치 확인**

THV 각 포인트들의 그래프를 봤을 때 26, 31, 35번 포인트가 다른 점들과 다른 분포를 띄고 있음을 알 수 있음.  26, 35번은 맹점이므로 31번을 중심적으로 바라본다.

* 보통 눈의 경우 주위 8개의 값과 비슷한 값을 띈다고 한다. 

  * 결과를 봤을 때, 측정이 제대로 이루어지지 않았음을 알 수 있다.

  > 31번 Point 주변 8개 Point 시각화 코드
  >
  > <img src = "https://user-images.githubusercontent.com/54921730/107759203-4f0b4900-6d6b-11eb-8fdc-88f370fe5b7d.png" width = 1000 max-width = 100% height = 500/>
  >
  > 시각화 결과
  >
  > <img src = "https://user-images.githubusercontent.com/54921730/107759396-972a6b80-6d6b-11eb-9ca0-8a6bdb24f1c7.png" width = 1000 max-width = 100% height = 400/>

**이상치 처리**

* THV 값이 제대로 측정이 되지 않았으므로 새로 구해준다.

  * TDV = THV - 일반인들의 평균이므로, 일반인들의 평균을 구해 THV 값을 채워줌

  * 같은 나이대의 사람들의 눈의 평균 값은 같아야 함. 

    * 따라서 THV - TDV를 하였을 때 같은 나이대 사람들의 최빈값을 평균이라고 두겠다.

    >THV - TDV 값들의 시각화
    >
    ><img src = "https://user-images.githubusercontent.com/54921730/107760568-503d7580-6d6d-11eb-90d1-10ee9bbb4636.png" width = 1000 max-width = 100% height = auto/>
    >
    >THV - TDV의 값들을 평균값으로 바꿔준 함수
    >
    ><img src = "https://user-images.githubusercontent.com/54921730/107761078-1faa0b80-6d6e-11eb-934a-8c456babf826.png" width = 1000 max-width = 100% height = auto/>
    >
    >정상적인 평균값과 TDV의 합으로 정상적인 THV 값들을 구해냄
    >
    ><img src = "https://user-images.githubusercontent.com/54921730/107761239-60a22000-6d6e-11eb-8e6f-3828e55b0e7e.png" width = 1000 max-width = 100% height = auto/>

## 데이터 전처리 완료







