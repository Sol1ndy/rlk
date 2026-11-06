# @s = the blast hazard (#hzEv 1 = the blast): the flash over the disc, the crack ring, the rocks.
execute unless score #hzEv mb matches 1 run return 0
execute at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/blast {r:12}
execute at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/p/rocks
execute at @s run function rlk:mboss/fieldgen/fx/snd/blast
