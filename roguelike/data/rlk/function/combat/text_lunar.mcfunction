# 달 피해 숫자 (위치 = 몹, @s = 몹). 자릿수를 하나씩 떼어 달빛 그라데이션 색으로(기울임). 치명타면 더 크게 + 초승달
data modify storage rlk:ln t set value {d0:"",d1:"",d2:"",d3:"",d4:"",d5:"",d6:"",d7:""}
data modify storage rlk:ln s set string storage rlk:combat dmg
data modify storage rlk:ln t.d0 set string storage rlk:ln s 0 1
data modify storage rlk:ln t.d1 set string storage rlk:ln s 1 2
data modify storage rlk:ln t.d2 set string storage rlk:ln s 2 3
data modify storage rlk:ln t.d3 set string storage rlk:ln s 3 4
data modify storage rlk:ln t.d4 set string storage rlk:ln s 4 5
data modify storage rlk:ln t.d5 set string storage rlk:ln s 5 6
data modify storage rlk:ln t.d6 set string storage rlk:ln s 6 7
data modify storage rlk:ln t.d7 set string storage rlk:ln s 7 8
data modify storage rlk:ln t.ox set from storage rlk:combat ox
data modify storage rlk:ln t.oy set from storage rlk:combat oy
data modify storage rlk:ln t.oz set from storage rlk:combat oz
data modify storage rlk:ln t.sc set value "1.55"
data modify storage rlk:ln t.moon set value ""
execute if score #crit tmp matches 1 run data modify storage rlk:ln t.sc set value "2.0"
execute if score #crit tmp matches 1 run data modify storage rlk:ln t.moon set value "☾ "
execute if score #lnEl tmp matches 7 run function rlk:combat/text_lunar_7 with storage rlk:ln t
execute if score #lnEl tmp matches 3 run function rlk:combat/text_lunar_3 with storage rlk:ln t
execute if score #lnEl tmp matches 5 run function rlk:combat/text_lunar_5 with storage rlk:ln t
