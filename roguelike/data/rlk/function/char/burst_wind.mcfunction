# 원소폭발 시전 시작 (@s = 플레이어, at 몸): #burstWind 틱 동안 이동·공격 불가 + 무적 + 화면 확대
scoreboard players operation @s buT = #burstWind tmp
execute if score #charN tmp matches 5 run scoreboard players set @s buT 40
execute if score #charN tmp matches 3 run scoreboard players set @s buT 28
scoreboard players operation @s dashInvT = @s buT
scoreboard players operation @s dashInvT += #burstInv tmp
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
execute if score @s bowT matches 1.. run function rlk:char/bow/cancel
# 이동 속도 -100%: 1인칭에서는 제자리에 서고, 시야가 좁아져 화면이 확대된다. 점프·넉백도 막는다
attribute @s minecraft:movement_speed modifier remove rlk:burst_cast
attribute @s minecraft:movement_speed modifier add rlk:burst_cast -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier remove rlk:burst_cast
attribute @s minecraft:jump_strength modifier add rlk:burst_cast -1 add_multiplied_total
attribute @s minecraft:knockback_resistance modifier remove rlk:burst_cast
attribute @s minecraft:knockback_resistance modifier add rlk:burst_cast 1 add_value
execute as @e[tag=rlk_av,limit=1] run attribute @s minecraft:knockback_resistance modifier add rlk:burst_cast 1 add_value
function rlk:view/stop_h
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 run execute unless score #k217 snd matches 1 run function rlk:snd/f240
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 run execute unless score #k218 snd matches 1 run function rlk:snd/f241
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 run particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.08 20

execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"burst"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"burst_metsu"}
