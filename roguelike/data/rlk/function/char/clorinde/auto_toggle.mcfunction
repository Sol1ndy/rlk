# 밤 순찰 중 좌클릭 (@s = 플레이어, at 몸): 자동 연사 켜기/끄기. 한 번의 클릭이 두 번 들어오는 것은 5틱 동안 무시
execute if score @s clTg matches 1.. run return 0
scoreboard players set @s clTg 5
execute if score @s clAuto matches 1 run return run function rlk:char/clorinde/auto_off
scoreboard players set @s clAuto 1
playsound minecraft:item.crossbow.loading_end master @s ~ ~ ~ 0.6 1.6
title @s actionbar {"text":"자동 사격 — 다시 좌클릭하면 멈춤","color":"#C58BFF"}
scoreboard players set @s hudHold 20
execute unless score @s atkCD matches 1.. run function rlk:char/clorinde/shoot
