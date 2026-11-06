# 「검신합일」 예약 (@s = 플레이어; player/take_damage = 맞음, player/dash_iframe = 대쉬로 흘려냄)
# 피해 처리 도중에는 새 피해를 주지 않는다: 다음 아이템 틱(hw_tick → hw_due)에서 반격(hw_ctr). 재사용 대기는 반격할 대상이 있을 때만 시작
# 흘려냄(dash_iframe: #dodged tmp 1)은 대쉬 자체의 무적 동안만(hw_dash 의 #hwDashEnd 까지): 원소폭발 · 추락 · 로노바 부활의 무적은
# 같은 dashInvT 를 쓰지만 대쉬가 아니라 반격하지 않는다. 맞은 타격(쓰러지는 타격 포함)은 그대로 예약
execute if score #dodged tmp matches 1 store result score #hwNow itv run time query gametime
execute if score #dodged tmp matches 1 unless score #hwNow itv <= #hwDashEnd itv run return 0
scoreboard players set #hwCtrQ itv 1
scoreboard players set #hwOn itv 1
scoreboard players set #hwWait itv 0
