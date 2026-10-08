# 시전 끝(발동·취소 공통): 움직임·시야 되돌리기 (@s = 플레이어)
scoreboard players set @s buT 0
attribute @s minecraft:movement_speed modifier remove rlk:burst_cast
attribute @s minecraft:jump_strength modifier remove rlk:burst_cast
attribute @s minecraft:knockback_resistance modifier remove rlk:burst_cast
execute as @e[tag=rlk_av,limit=1] run attribute @s minecraft:knockback_resistance modifier remove rlk:burst_cast
