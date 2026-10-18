# The pack-up begins (@s = body): the meter closes, low gravity and the damage cut end (the kit's meter, icon
# and hint leave the lines), the idle look.
scoreboard players set #fgOpen mb 0
scoreboard players set #fgLowG mb 0
function rlk:mboss/fieldgen/hud/kit_off
execute unless score #fgPat mb matches 22 run function rlk:mboss/fieldgen/rig/look/idle
function rlk:mboss/fieldgen/hud/refresh
