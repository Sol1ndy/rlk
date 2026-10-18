# @s = body: stop whatever runs (hazards, props, pull, movement, the slot pattern, the break / groggy / recovery)
# and re-derive the rig and the hitbox from the field stage (butterfly S3: never a stale rig form).
function rlk:mboss/lib_clear
function rlk:mboss/fieldgen/p/cancel
function rlk:mboss/fieldgen/rig_stub/prop/clear
scoreboard players set #fgMv mb 0
scoreboard players set #fgBrkQ mb 0
execute if score #fgSt mb matches 3..6 run scoreboard players set #fgCrack mb 0
# a cut field opening (invisible, untargetable, maybe not at the centre yet) finishes at once
execute if score #fgField mb matches 1 run function rlk:mboss/fieldgen/field/up
execute if score #fgField mb matches 2.. run function rlk:mboss/fieldgen/field/rig_f
execute if score #fgField mb matches 0 run function rlk:mboss/fieldgen/field/rig_c
function rlk:mboss/fieldgen/u/crack_d
scoreboard players set #fgCool mb 10
function rlk:mboss/fieldgen/ai/enter
