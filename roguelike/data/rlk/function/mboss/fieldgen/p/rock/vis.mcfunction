# @s = a burst (#hzEv 1 = it strikes).
execute unless score #hzEv mb matches 1 run return 0
execute if score @s mbHzV matches 61 at @s run function rlk:mboss/fieldgen/fx/p/floor_burst
execute if score @s mbHzV matches 61 at @s run function rlk:mboss/fieldgen/fx/snd/floor_burst
