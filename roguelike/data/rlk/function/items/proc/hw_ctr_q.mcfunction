# 「검신합일」 예약 (@s = 플레이어; player/take_damage = 맞음(1 · 2단계 패링 포함), player/def/judge = 닷지(퍼펙트 · 넓은 창) 또는
# 퍼펙트 패링으로 흘려냄). 원소폭발 · 추락 · 로노바 부활의 무적(dashInvT)으로 피한 것은 부르지 않는다(player/def/inv)
# 피해 처리 도중에는 새 피해를 주지 않는다: 다음 아이템 틱(hw_tick → hw_due)에서 반격(hw_ctr). 재사용 대기는 반격할 대상이 있을 때만 시작
scoreboard players set #hwCtrQ itv 1
scoreboard players set #hwOn itv 1
scoreboard players set #hwWait itv 0
