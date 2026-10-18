# Hook tick (@s = body, at @s, fight state). Order: clocks and flags; the break meter (a count from on_hit,
# the 20th breaks the field before the AI runs: the running pattern is cancelled); the field clocks; the
# body clamp r 16.5; AI state; pattern slot; the low-gravity request (mboss/main clears #mbLowG every tick,
# so it is set again every tick the field holds it, after the slot: the banner tick counts); then the rig.
scoreboard players add #fgClk mb 1
execute if score #fgFlash mb matches 1 run function rlk:mboss/fieldgen/rig_stub/flash
scoreboard players set #fgFlash mb 0
execute if score #fgBrkFx mb matches 1 run function rlk:mboss/fieldgen/brk/count
execute if score #fgBrkQ mb matches 1 run function rlk:mboss/fieldgen/brk/begin
execute if score #fgPipT mb matches 1.. run function rlk:mboss/fieldgen/hud/pip_tick
execute if score #fgField mb matches 1.. run function rlk:mboss/fieldgen/field/tick
execute unless entity @s[tag=rlk_mb_mv] positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] run function rlk:mboss/fieldgen/u/leash
function rlk:mboss/fieldgen/ai/state
execute if score #fgPat mb matches 1.. run function rlk:mboss/fieldgen/p/run
execute if score #fgLowG mb matches 1 run scoreboard players set #mbLowG mb 1
function rlk:mboss/fieldgen/rig_stub/tick
