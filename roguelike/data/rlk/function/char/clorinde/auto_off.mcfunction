# 자동 연사 끄기 (@s = 플레이어)
execute unless score @s clAuto matches 1 run return 0
scoreboard players set @s clAuto 0
playsound minecraft:block.lever.click master @s ~ ~ ~ 0.5 0.8
