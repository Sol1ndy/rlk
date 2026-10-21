# @s = body, idle (no main-slot pattern): cooldown, idle tracking (<= 3 deg/t within +-45 degrees), the module leash
# to the body disc, the next decision.
execute if score #azCool mb matches 1.. run scoreboard players remove #azCool mb 1
execute if score #azF45 mb matches 1 unless score #azNoTurn mb matches 1 run function rlk:mboss/mv/turn {max:3}
execute positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..8,limit=1] run function rlk:mboss/azhdaha/ai/leash
execute if score #azCool mb matches ..0 run function rlk:mboss/azhdaha/ai/next
