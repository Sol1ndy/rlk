function rlk:cm/sh/face
scoreboard players set @s cmS 3
# A rush crosses the player and spends its damage check only once.
tag @s remove rlk_sh_rhit
scoreboard players set @s cmT 20
function rlk:cm/pose_s
execute unless score #k102 snd matches 1 run function rlk:snd/f109
