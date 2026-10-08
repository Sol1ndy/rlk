# 원소폭발 시전 시작 (@s = 플레이어, at 몸): #burstWind 틱 동안 이동·공격 불가 + 무적 + 화면 확대
scoreboard players operation @s buT = #burstWind tmp
scoreboard players operation @s dashInvT = #burstWind tmp
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
playsound minecraft:block.beacon.activate master @a ~ ~ ~ 0.8 1.7
playsound minecraft:item.trident.return master @a ~ ~ ~ 0.7 0.7
particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.08 20
