# FN-cam: the first held tick (@s = the player): the hold tag (view/tick rests while it is on: no avatar move, no aim,
# no re-seat), the game mode to give back (a tag: survival / creative; neither = adventure), the place to return to (the
# avatar's, kept in storage because a /reload removes the avatar), the sprint FOV modifier off, the F5 crosshair title
# blanked (unless an overlay title is up: vBig), then spectator mode (which dismounts the player from the F5 seat).
tag @s add rlk_mb_camh
tag @s remove rlk_mb_cgS
tag @s remove rlk_mb_cgC
execute if entity @s[gamemode=survival] run tag @s add rlk_mb_cgS
execute if entity @s[gamemode=creative] run tag @s add rlk_mb_cgC
data remove storage rlk:mboss camret
execute store result storage rlk:mboss camret.x double 0.01 run data get entity @e[tag=rlk_av,limit=1] Pos[0] 100
execute store result storage rlk:mboss camret.y double 0.01 run data get entity @e[tag=rlk_av,limit=1] Pos[1] 100
execute store result storage rlk:mboss camret.z double 0.01 run data get entity @e[tag=rlk_av,limit=1] Pos[2] 100
execute if score #spr view matches 1 run attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
scoreboard players set #spr view 0
execute unless score @s vBig matches 1.. run title @s title {text:""}
gamemode spectator @s
