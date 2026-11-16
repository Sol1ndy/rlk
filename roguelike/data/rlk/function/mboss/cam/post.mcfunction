# FN-cam: the reward of the tick advancement rlk:mboss/cam_post (@s = the player, inside the game's own player tick, right after
# it snapped a spectating player to the camera and ended the spectate of a sneaking one; armed by mboss/cam/hold every
# held tick, so it costs nothing outside a lock). While re-sends are asked for (the first ticks of a hold, a module's
# cam_resend, a movement key): the camera is given to the player and back, which sends the camera packet again - a
# client that ignored the first one (it did not have the entity yet) is attached now. Then the live camera is spectated:
# a sneaking player is back on it before the tick ends (the client gets both packets in one batch).
execute unless entity @s[tag=rlk_mb_camh] run return 0
execute unless score #mbCam mb matches 1 run return 0
execute unless entity @s[gamemode=spectator] run return 0
execute if score #mbCamRe mb matches 1.. run spectate
execute if score #mbCamRe mb matches 1.. run scoreboard players remove #mbCamRe mb 1
execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1]
spectate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1]
