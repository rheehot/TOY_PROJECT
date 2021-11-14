# TOY_PROJECT
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



* # 행동의 이유들
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



  0.99%까지 갔다가 -1%로 가거나, -0.99%까지 갔다가 1%로 가는 경우는 거의 없다고 생각했음 



  구매가 일부만 되는 문제 해결방법 두 가지.

  80%의 성공만 life에 반영하게?

  거래 데이터 형식, 거래 데이터를 모으는 이유: 구매시점에 따른 성공률, 코인크기에 따른 성공률등을 계싼해보기 위함이다

  한틱의 가격이 0.33%일 때 최대 0.32%의 lisk를 감수해야 한다

  2021-11-09: sell_process변경 // 이유: ~라

  게임이 종료되면 TEST환경을 진행한다? -> 여기서도 손해를 보는 위험은 여전히 존재함 // 더 많은 정보를 수집할 수 있는 장점

  검증이 필요한 가설: 비슷한 가격대에 구매한 코인의 결과는 같다?

  분산투자를 하지 않은 이유:
   10%로 한다 가정했을때
   해봤었다, 그걸로 1%수익낼려면 ... 다.
   55%의 확률로 1%의 수익을, 나머지 45%의 확률로 -1%의 수익(1%의 손해)을 가져오는 알고리즘으로 전체자산의 10%씩 분산투자하면
   하루 1%의 수익을 내기 위해 !@#번의 거래를 해야 한다.

  # 가독성 높이는 방법?
  * ## 이렇게 하면 괜찮아?
    * 예비비는 총액으로 국회의 의결을 얻어야 한다. 예비비의 지출은 차기국회의 승인을 얻어야 한다. 법관이 중대한 심신상의 장해로 직무를 수행할 수 없을 때에는 법률이 정하는 바에 의하여 퇴직하게 할 수 있다. 대법원과 각급법원의 조직은 법률로 정한다. 국가안전보장회의의 조직·직무범위 기타 필요한 사항은 법률로 정한다. 중앙선거관리위원회는 법령의 범위안에서 선거관리·국민투표관리 또는 정당사무에 관한 규칙을 제정할 수 있으며, 법률에 저촉되지 아니하는 범위안에서 내부규율에 관한 규칙을 제정할 수 있다. 국회는 국무총리 또는 국무위원의 해임을 대통령에게 건의할 수 있다. 공공필요에 의한 재산권의 수용·사용 또는 제한 및 그에 대한 보상은 법률로써 하되, 정당한 보상을 지급하여야 한다.
