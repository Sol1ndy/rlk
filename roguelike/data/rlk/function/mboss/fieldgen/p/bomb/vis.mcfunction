# @s = a C1 hazard (#hzEv 1 = its strike): 11 / 13 a bomb (11 with the burst sound: every 2nd bomb),
# 12 the finisher slam.
execute unless score #hzEv mb matches 1 run return 0
execute if score @s mbHzV matches 11 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/bomb_burst
execute if score @s mbHzV matches 11 at @s run function rlk:mboss/fieldgen/fx/snd/bomb_burst
execute if score @s mbHzV matches 13 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/bomb_burst
execute if score @s mbHzV matches 12 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/slam
execute if score @s mbHzV matches 12 at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/dust_puff
execute if score @s mbHzV matches 12 at @s run function rlk:mboss/fieldgen/fx/snd/slam
