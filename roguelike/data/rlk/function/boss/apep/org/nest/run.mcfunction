# @s = a 둥지: 1 flying (keeps 4-8 b from the player at 0.15 b/t; blinks to 5 b when > 12 b), 2 the wall cast
# (12 t loop pose = the tell; walls at 12), 3 the blink (6 t). No attack.
execute if score @s apS matches 2 run return run function rlk:boss/apep/org/nest/cast
execute if score @s apS matches 3 run return run function rlk:boss/apep/org/nest/blink
function rlk:boss/apep/org/nest/fly
