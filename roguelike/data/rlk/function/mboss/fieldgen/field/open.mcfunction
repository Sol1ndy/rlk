# Field opening clock 35 (@s = body): the unfold; targetable again; the meter opens at 0/20 (crack 0;
# the kit's meter on the sub-line), the field look, the field hitbox, the field damage cut
# (60 %), the first field's clock #fgFirstT from 0. No hint on the lines (10-21 user rule: no how-to-fight
# advice). Idempotent (fix round FG-S2): a meter already open (a reload or test cut of the opening after the
# unfold, a test request inside the field) keeps its count, its field number and its clock; only the look, the
# hitbox and the lines are applied again.
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
scoreboard players set #fgFirstT mb 0
function rlk:mboss/fieldgen/fx/hud/meter_open
function rlk:mboss/fieldgen/seq_f/unfold
function rlk:mboss/fieldgen/hud/refresh
