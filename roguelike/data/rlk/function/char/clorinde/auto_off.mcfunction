# 자동 연사 끄기 (@s = 플레이어)
execute unless score @s clAuto matches 1 run return 0
scoreboard players set @s clAuto 0
execute unless score #k254 snd matches 1 run function rlk:snd/f283
