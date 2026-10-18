# @s = a missile decal (#hzEv 1 = its impact).
execute unless score #hzEv mb matches 1 run return 0
execute at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/missile_impact
execute at @s run function rlk:mboss/fieldgen/fx/snd/missile_impact
