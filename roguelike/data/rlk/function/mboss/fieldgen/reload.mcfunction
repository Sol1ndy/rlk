# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, hazards, props, markers). HP and
# the module scores are kept; the state is re-derived from them (butterfly S3 / S4: nothing is assumed):
#   a break in progress -> a fresh groggy; a groggy goes on; a recovery ends (cruise);
#   the field opening (pattern 20) -> the field up at the centre (meter open, low gravity), the opening waves;
#   the pack-up (22) -> cruise; any other field stage resumes at the centre (the AI restarts that stage).
function rlk:mboss/fieldgen/ai/consts
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
scoreboard players set #fgX mb 0
execute if score #fgSt mb matches 6 run scoreboard players set #fgX mb 1
execute if score #fgPat mb matches 20 run scoreboard players set #fgX mb 2
execute if score #fgField mb matches 1 run scoreboard players set #fgX mb 2
execute if score #fgPat mb matches 22 run scoreboard players set #fgX mb 3
execute if score #fgField mb matches 5 run scoreboard players set #fgX mb 3
function rlk:mboss/fieldgen/p/cancel
scoreboard players set #mbNoLeash mb 0
scoreboard players set #fgMv mb 0
scoreboard players set #fgBrkQ mb 0
scoreboard players set #fgBrkFx mb 0
tag @s remove rlk_mb_inv
function rlk:mboss/fieldgen/rig_stub/init
function rlk:mboss/fieldgen/rig_stub/spawn
execute if score #fgX mb matches 1 run function rlk:mboss/fieldgen/field/drop
execute if score #fgX mb matches 2 run function rlk:mboss/fieldgen/field/up
execute if score #fgX mb matches 3 run function rlk:mboss/fieldgen/field/now_c
execute if score #fgField mb matches 2..4 run function rlk:mboss/fieldgen/field/rig_f
execute if score #fgField mb matches 0 run function rlk:mboss/fieldgen/field/rig_c
function rlk:mboss/fieldgen/u/crack_d
execute if score #fgX mb matches 1 run return run function rlk:mboss/fieldgen/groggy/begin
execute if score #fgSt mb matches 3 run return run function rlk:mboss/fieldgen/groggy/rig
execute if score #fgSt mb matches 4 run return run function rlk:mboss/fieldgen/recover/end
scoreboard players set #fgCool mb 20
function rlk:mboss/fieldgen/ai/enter
