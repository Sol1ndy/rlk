# FN-cam: the first held tick (@s = the player): the hold tag (view/tick rests while it is on: no avatar move, no aim,
# no re-seat), the game mode to give back (a tag: survival / creative; neither = adventure), the place to return to (the
# avatar's, kept in storage because a /reload removes the avatar), the sprint FOV modifier off, the F5 crosshair title
# blanked (unless an overlay title is up: vBig), the sidebar off, then spectator mode (which dismounts the player from the
# F5 seat) and the seat removed (an armour stand: a spectator would see its ghost; mboss/cam/back makes it again).
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
scoreboard objectives setdisplay sidebar
# A left click of a spectator spectates the entity under the pick ray (the avatar, the boss body): both ranges forced to
# 0 (total x (1 - 1): the base and the other modifiers stay) make every pick a miss on the client; nothing is sent.
attribute @s minecraft:entity_interaction_range modifier add rlk:mb_cam -1 add_multiplied_total
attribute @s minecraft:block_interaction_range modifier add rlk:mb_cam -1 add_multiplied_total
# The player's own F5 picture = the shot's, should the client ever draw a frame from it (between the two camera packets
# of a re-send): the game keeps a spectating player at the camera entity with its rotation; scale 0.0625 x 2 = 0.125 and
# camera distance 0 + 32 pull the own view back 0.125 x 32 = 4 blocks, as a display camera's.
attribute @s minecraft:scale modifier add rlk:mb_cam 1 add_multiplied_total
attribute @s minecraft:camera_distance modifier add rlk:mb_cam 32 add_value
execute unless score #mbCamRe mb matches 3.. run scoreboard players set #mbCamRe mb 3
scoreboard players set #mbCamIn mb 0
scoreboard players set #mbCamSap mb 0
gamemode spectator @s
kill @e[tag=rlk_vseat]
