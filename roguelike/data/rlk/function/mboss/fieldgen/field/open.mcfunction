# Field opening clock 35 (@s = body): the unfold; targetable again; the meter opens at 0/20 (crack 0),
# the field look, the field hitbox, the field damage cut (60 %), the first field's hint for 120 t.
tag @s remove rlk_mb_inv
scoreboard players set #fgOpen mb 1
scoreboard players set #fgBrk mb 0
scoreboard players set #fgBrkT mb -1000000
scoreboard players set #fgBrkFx mb 0
scoreboard players set #fgBrkQ mb 0
scoreboard players set #fgCrack mb 0
scoreboard players set #fgPipT mb 0
function rlk:mboss/fieldgen/rig_stub/crack/0
function rlk:mboss/fieldgen/rig_stub/look/field
function rlk:mboss/fieldgen/form/hitbox_f
scoreboard players add #fgFN mb 1
scoreboard players set #fgHintT mb 0
function rlk:mboss/fieldgen/cfx/unfold_f
function rlk:mboss/fieldgen/hud/refresh
