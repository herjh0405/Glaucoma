# 인공지능을 활용한 녹내장 예측 연구(Glaucoma prediction with AI) 
부산대학교 산업수학센터 박정례 박사님 지도 아래서 연구 수행 중 (2021.01.06 ~ )

**1. 선행 연구 논문 이해** (2021.01.06 ~ 2021.01.12)
- **Visual Field prediction using Recurrent Neural Network**(Park, K., Kim, J., & Lee, J. (2019). *Scientific Reports*, *9*(1), 1–12.) [link](https://doi.org/10.1038/s41598-019-44852-6) 

   - 기존의 OLR 보다 RNN 이 성능이 더 좋음을 확인
   - 참고 논문 리뷰 - 박정례 박사님 [file](https://github.com/herjh0405/Glaucoma/blob/master/Paper_review/(2019)%20Visual%20Field%20prediction%20using%20Recurrent%20Neural%20Network.md)
   
**2. 두 병원의 데이터 전처리** (2021.01.13 ~ 2021.01.20) 
   - 부산소재지 ㄷ병원과 ㅂ병원의 데이터 통일화 [data](https://github.com/herjh0405/Glaucoma/blob/master/sample2.csv)
      - 데이터 유출의 위험 때문에 차트번호 -> 랜덤화, 생년월일 -> 검사 당시 연령, 이름 -> 삭제
   
**3. Data Visualization** (2021.01.21 ~ 2021.01.27) 
   - 이상치 데이터 시각화로 체크 (Violinplot) [file](https://github.com/herjh0405/Glaucoma/blob/master/001.Data_PreProcessing%26Visualization.ipynb)
      - THV를 제외한 나머지 검진에서 26번과 35번 데이터가 맹점으로써 없는 것을 확인
      - 특이 데이터는 추후 박사님과 논의 예정

**4. Linear Regression Model** (2021.01.28 ~ 2021.02.03) 
   - 이전 논문에서 시행하였던 선형회귀 모델 구현 [file](http://localhost:8888/notebooks/github/Glaucoma/002.Linear_Regression.ipynb)
      - 환자의 ID와 원하는 검진값을 입력하면 화면에 띄워주는 함수 생성
         - OD에 관해서만 하였고 OS는 추후에 조금 더 고민할 예정, THV도 보여줄 것
