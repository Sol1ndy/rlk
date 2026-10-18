# Field opening clock 35 (@s = body): the unfold; targetable again; the meter opens at 0/20 (crack 0;
# the kit's meter on the sub-line), the field look, the field hitbox, the field damage cut
# (60 %), the first field's hint for 120 t (the kit's hint_on / hint_off). Idempotent (fix round FG-S2): a
# meter already open (a reload or test cut of the opening after the unfold, a test request inside the field)
# keeps its count, its field number and its hint; only the look, the hitbox and the lines are applied again.
tag @s remove rlk_mb_inv
execute if score #fgOpen mb matches 1 run return run function rlk:mboss/fieldgen/field/reopen
scoreboard players set #fgOpen mb 1
scoreboard players set #fgBrk mb 0
scoreboard players set #fgBrkT mb -1000000
scoreboard players set #fgBrkFx mb 0
scoreboard players set #fgBrkQ mb 0
scoreboard players set #fgCrack mb 0
function rlk:mboss/fieldgen/rig/crack/0
function rlk:mboss/fieldgen/rig/look/field
function rlk:mboss/fieldgen/form/hitbox_f
scoreboard players add #fgFN mb 1
scoreboard players set #fgHintT mb 0
function rlk:mboss/fieldgen/fx/hud/meter_open
execute if score #fgFN mb matches 1 run function rlk:mboss/fieldgen/fx/hud/hint_on
function rlk:mboss/fieldgen/seq_f/unfold
function rlk:mboss/fieldgen/hud/refresh
