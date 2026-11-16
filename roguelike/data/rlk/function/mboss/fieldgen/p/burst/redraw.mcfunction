# After a pause (@s = body): the blast hazard (hz_vis 51), unless it struck already, gets its decals again.
execute as @e[type=minecraft:marker,tag=rlk_mb_hzq,scores={mbHzV=51}] if score @s mbHzT < @s mbHzW at @s run function rlk:mboss/fieldgen/p/burst/redraw1
