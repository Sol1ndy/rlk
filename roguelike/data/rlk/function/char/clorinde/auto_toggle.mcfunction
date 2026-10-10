# 밤 순찰 중 좌클릭 (@s = 플레이어, at 몸): 자동 연사 켜기/끄기. 한 번의 클릭이 두 번 들어오는 것은 5틱 동안 무시
execute if score @s clTg matches 1.. run return 0
scoreboard players set @s clTg 5
execute if score @s clAuto matches 1 run return run function rlk:char/clorinde/auto_off
scoreboard players set @s clAuto 1
execute unless score #k261 snd matches 1 run function rlk:snd/f292
execute unless score @s atkCD matches 1.. run function rlk:char/clorinde/shoot
