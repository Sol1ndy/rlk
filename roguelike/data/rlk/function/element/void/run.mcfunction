# 예약된 공허 반응 발동 (@s = 몹, at @s). #q = 반응 번호, #qDmg = 피해(또는 방어막량), #qEl = 원소
execute if score #q tmp matches 17 run function rlk:element/void/run_burn
execute if score #q tmp matches 18 run function rlk:element/void/run_abyss
execute if score #q tmp matches 19 run function rlk:element/void/run_judg
execute if score #q tmp matches 20 run function rlk:element/void/run_frost
execute if score #q tmp matches 21 run function rlk:element/void/run_cryst
execute if score #q tmp matches 22 run function rlk:element/void/run_vac
execute if score #q tmp matches 23 run function rlk:element/void/run_bloom
