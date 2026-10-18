# @s = the slam hazard (#hzEv 1 = the impact).
execute unless score #hzEv mb matches 1 run return 0
execute if score @s mbHzV matches 21 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/slam
execute if score @s mbHzV matches 21 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/dust_puff
execute if score @s mbHzV matches 21 at @s run function rlk:mboss/fieldgen/fx/snd/slam
