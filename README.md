# 가상화폐 자동거래 시스템
* # 코드리뷰
  * ## 비동기 방식으로 Sell과 Buy가 진행된다

  * ## Sell
    ```python
     while True:
      if len(balances)>2: #KRW,거래불가코인 을 제외한 코인이 있다면
         새롭게 구매된 종목은 check_lst에 넣고
         check_lst의 종목이 팔렸으면 done_lst에 넣는다
         if 현재가격이 -1%로 떨어졌다면:
            바로 시장가 판매
    ```


  * ## Buy
    ```python
     while True: #계속 반복됨
      for i in coin_lst #모든 코인이름을 순회하면서
         coin = get_ohlcv() #분봉 데이터를 15개 가져온다
         coin의 BOP,MFI,Sto,RSI를 계산해서 coin의 column으로 추가한 뒤
         if BOP,MFI,Sto,RSI가 모두 특정 조건을 만족하면:
            ret = get_order #구매주문을 넣고
            await asyncio.sleep(15) #15초간 대기한다
            if int(float(result['remaining_volume'])) != 0 : #구매가 진행되지 않았으면
               ret = cancel_order(ret['uuid']) #구매주문을 넣어둔 걸 취소한다
            else:
               limit_order = sell_limit_order #곧바로 1% 예약주문을 걸어둠
    ```   

   * ## Upbit_tools.py
     * asset(): 현재 보유 자산을 return 합니다
     * one_tick(price): 가격대별로 한 틱의 가격이 얼마인지 계산합니다
     * market_status(): '전일대비 가격이 상승한 종목의 개수 - 전일대비 가격이 하락한 종목의 개수'를 return 합니다 
     * sell_price(current_price,buy_price,under_k): 현재가격을 기준으로 1%의 수익을 내는 거래가능 가격을 return 합니다

* # 생각 정리
  * ## 주식이 아닌 가상화폐를 선택한 이유 
     * 잘 구현된 API 
     * 큰 변동성

  * ## 분산투자를 진행하지 않은 이유
   * 1%의 수익을 위해 너무 많은 거래가 필요하기 때문입니다
     * 가령 55%의 확률로 1%의 수익을, 나머지 45%의 확률로 -1%의 수익을 가져오는 알고리즘이 있고
     * 위 알고리즘으로 한번 거래할때마다 전체자산의 10%를 사용한다고 가정했을 때
     * 하나의 거래가 성공하면 전체 잔액의 0.1%의 수익을 올리는 것임
     * 1%의 수익과 1%의 손해가 동등하게 상세된다고 가정했을 때(실제로 손해의 힘이 더 큼: 1.01x0.99 = 0.9999) 수익의 개수가 10개 더 많아야 함
     * 그러면 100번의 거래를 해야 (+55-45) 1%의 수익이 달성됨
     * 근데만약 성공률이 51%다? 그러면 500번 거래해야 ((51-49)x5) 1%의 수익이 달성됨


  * ## 지정가로 거래하는 이유
     * 0.33%인 경우 // 존재하지 않지만 0.99%인 경우
     * 시장가 거래는 빠른 대신 한틱 낮게 거래될 가능성이 크다

  * ## -1%의 손해를 설정한 이유
     * 일단 손절이 없는건 말이 안됨
     * 99%의 확률로 x10의 수익을, 나머지 1%의 확률이 x0을 가져온다고 했을 때 무한히 많이 시행하면 결국 내 잔고는 0원이 된다
     * -1%의 기준은 임의로 내가 정한거지만 -2%가 되었을 때에는 너무많은 거래가 필요함

  * ## LIFE의 개념을 도입한 이유
    * 좋은날과 나쁜날이 있다는 가정 때문임 // 데이터로 봤을 때 그런게 

  * ## 데이터를 수집하는 이유
    * 구입시간에 따른 유의미 차이
    * 종목에따른 유의미차이
    * 
  * ## 구매 알고리즘
    * 가장 중요하면서도 어려운 것 (이게 확실하다면 시스템을 개발할 필요 없이 24시간 모니터 앞에 앉아있어도 억만장자가 될 수 있다
    * 완벽한 구매방법이 존재한다는 생각을 버리고 조금이라도 익절을 할 가능성이 크다면 이를 극대화하는 방향으로
    * 직접 구매한 데이터를 2차 분석해 이를 가공할 예정
    * rsi가 상승하는 시그널을 보고 사면 괜찮을까?



  * ## 시간대가 유의미한가?
![Figure 2022-01-01 172624](https://user-images.githubusercontent.com/25142537/147846886-ea0c8e9d-11d8-4215-9a61-587f3a3bbef4.png)

   * 시간대가 유의미 하다면 뭐 때문에 그런걸까?
     * 사람들의 일정한 루틴에 의해? (ex- 출근할 때 확인한다, 점심시간에 확인한다 등)
     * 세력이 활동하는 시간이다?
     * 내가 모르는 어떠한 인과에 의해?
     * 사실 아무런 관련이 없고 우연의 일치이다?
     * 우선 9시는 확실히 유의미하다고 느낌 (거래 경험을 통해)
