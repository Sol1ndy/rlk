# 퍼펙트 닷지의 박자, 실제 틱 #btA (beat/clock). 멈춘 틱 1 · 6 · 7 · 9 · 10 · 12 · 13, 맞지 않는 틱 1~14
scoreboard players set #btHold cb 0
execute if score #btOn tmp matches 1 if score #btA cb matches 1 run scoreboard players set #btHold cb 1
execute if score #btOn tmp matches 1 if score #btA cb matches 6..7 run scoreboard players set #btHold cb 1
execute if score #btOn tmp matches 1 if score #btA cb matches 9..10 run scoreboard players set #btHold cb 1
execute if score #btOn tmp matches 1 if score #btA cb matches 12..13 run scoreboard players set #btHold cb 1
scoreboard players set #btInv cb 0
execute if score #btOn tmp matches 1 if score #btA cb matches 1..14 run scoreboard players set #btInv cb 1
function rlk:player/def/beat/apply
execute if score #btA cb matches 1..20 at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_ember
execute if score #btA cb matches 3 at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_chime
execute if score #btA cb matches 5 as @a[tag=player,limit=1] run function rlk:char/motion/beat/dodge
execute if score #btA cb matches 6 as @a[tag=player,limit=1] unless score @s devMode matches 1 run attribute @s minecraft:movement_speed modifier add rlk:beat_fov -0.06 add_multiplied_total
execute if score #btA cb matches 14 run function rlk:player/def/beat/d/a14
execute if score #btA cb matches 21 run function rlk:player/def/beat/d/a21
execute if score #btA cb matches 27.. run function rlk:player/def/beat/end
