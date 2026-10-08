# 조준 시작 (@s = 플레이어, at 몸): 움직일 수 없음(+ 화면 확대) · 우산총
scoreboard players set @s nvA 1
scoreboard players set @s nvGap 0
scoreboard players set @s dashMoveT 0
attribute @s minecraft:movement_speed modifier remove rlk:navia_aim
attribute @s minecraft:movement_speed modifier add rlk:navia_aim -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier remove rlk:navia_aim
attribute @s minecraft:jump_strength modifier add rlk:navia_aim -1 add_multiplied_total
function rlk:view/stop_h
function rlk:char/navia/gun_spawn
kill @e[tag=rlk_nvopen]
playsound minecraft:item.crossbow.loading_start master @a ~ ~ ~ 0.8 0.8
playsound minecraft:block.chain.place master @a ~ ~ ~ 0.6 1.2
