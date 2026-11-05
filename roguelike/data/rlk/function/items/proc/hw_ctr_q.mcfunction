# 「검신합일」 예약 (@s = 플레이어; player/take_damage = 맞음, player/dash_iframe = 대쉬로 흘려냄)
# 피해 처리 도중에는 새 피해를 주지 않는다: 다음 아이템 틱(hw_tick → hw_due)에서 반격(hw_ctr). 재사용 대기는 반격할 대상이 있을 때만 시작
scoreboard players set #hwCtrQ itv 1
scoreboard players set #hwOn itv 1
scoreboard players set #hwWait itv 0
