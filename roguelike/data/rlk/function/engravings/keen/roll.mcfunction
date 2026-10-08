# 치명타 판정 직후 (@s = 플레이어, #crit = 판정 결과). 치명타가 났으면 다음 1회를 확정 치명타로 예약(쿨타임), 예약이 있으면 이번에 사용
execute unless score keen engN matches 6.. run return 0
execute if score #crit tmp matches 0 if score @s keenNext matches 1 run return run function rlk:engravings/keen/use
execute if score #crit tmp matches 1 unless score @s keenCd matches 1.. run function rlk:engravings/keen/arm
