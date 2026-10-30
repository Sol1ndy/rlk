# @s = body, idle (no main-slot pattern, not in a cine; phases 1 and 3): cooldown, idle tracking (phase 1 <= 3 deg/t
# within 60 degrees, else a crab-turn step for a player outside BACK; phase 3 <= 3 deg/t always), the module leash
# to the idle disc r 14 at 0.13 b/t, the next decision.
execute if score #apCool mb matches 1.. run scoreboard players remove #apCool mb 1
execute if score #apPh mb matches 3 run function rlk:mboss/mv/turn {max:3}
execute if score #apPh mb matches 1 unless score #apWide mb matches 1 run function rlk:mboss/mv/turn {max:3}
execute if score #apPh mb matches 1 if score #apWide mb matches 1 unless score #apZone mb matches 4 if score #apCool mb matches 5.. unless score #apLastMv mb matches 1 run return run function rlk:boss/apep/ai/step_go
execute positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..14,limit=1] run function rlk:boss/apep/ai/leash
execute if score #apCool mb matches ..0 run function rlk:boss/apep/ai/next
