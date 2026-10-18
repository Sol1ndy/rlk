# @s = body, after the break (or a reload / test): 200 t slumped (ring centre about 3 b, core on the floor):
# hittable, no attacks, no tracking. The cruise counters restart here (4 patterns to the next field; a
# test cut of the groggy keeps them: butterfly S8). No damage bonus.
scoreboard players set #fgSt mb 3
scoreboard players set #fgT mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #fgMv mb 0
scoreboard players set #fgBrk mb 0
scoreboard players set #fgCruN mb 0
scoreboard players set #fgCruLim mb 4
function rlk:mboss/fieldgen/hud/groggy_on
function rlk:mboss/fieldgen/groggy/rig
function rlk:mboss/fieldgen/cfx/groggy
function rlk:mboss/fieldgen/hud/refresh
