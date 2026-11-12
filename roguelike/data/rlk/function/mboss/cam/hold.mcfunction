# FN-cam, from rlk:tick right after mboss/main while #mbCam mb is 1 (@s = the tagged player): the player watches the
# live camera (#mbCamId mb 1 = rlk_mb_cam1, 2 = rlk_mb_cam2) in spectator mode.
# No fight any more (the request outlived it): the request is dropped and the player released.
execute unless score #mbLive mb matches 1 run scoreboard players set #mbCam mb 0
execute unless score #mbLive mb matches 1 run return run function rlk:mboss/cam/release
# The player is their own body (developer mode; the tick after a relog or a /reload rebuilt the view: no avatar to
# leave behind): never locked, and a player who still carries the hold from before is released.
execute if entity @s[tag=rlk_body] run return run function rlk:mboss/cam/release
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:mboss/cam/release
# The live camera is gone (killed): the player is not left a free spectator; the lock comes back with the camera.
execute if score #mbCamId mb matches 2 unless entity @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run return run function rlk:mboss/cam/release
execute unless score #mbCamId mb matches 2 unless entity @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run return run function rlk:mboss/cam/release
execute unless entity @s[tag=rlk_mb_camh] run function rlk:mboss/cam/hold_in
# The game's own player tick runs after every function and ends a spectate while Shift is down (ServerPlayer.tick:
# wantsToStopRiding -> setCamera(self)); right after that it fires the `tick` advancement trigger. Revoking the
# advancement arms it for this tick: its reward mboss/cam/post spectates again in the same server tick.
advancement revoke @s only rlk:mboss/cam_post
# A movement key held (a client that is not on the camera could fly with it): the camera is re-sent for real on the
# first tick and then every fourth tick of the press (mboss/cam/post). Shift needs nothing here: the game itself takes the
# camera away and post gives it back, every tick.
scoreboard players set #mbCamK mb 0
execute if predicate rlk:in_f run scoreboard players set #mbCamK mb 1
execute if predicate rlk:in_b run scoreboard players set #mbCamK mb 1
execute if predicate rlk:in_l run scoreboard players set #mbCamK mb 1
execute if predicate rlk:in_r run scoreboard players set #mbCamK mb 1
execute if predicate rlk:in_jump run scoreboard players set #mbCamK mb 1
execute if score #mbCamK mb matches 0 run scoreboard players set #mbCamIn mb 0
execute if score #mbCamK mb matches 1 run scoreboard players add #mbCamIn mb 1
execute if score #mbCamIn mb matches 5.. run scoreboard players set #mbCamIn mb 1
execute if score #mbCamIn mb matches 1 unless score #mbCamRe mb matches 1.. run scoreboard players set #mbCamRe mb 1
# `spectate` every tick: it sends nothing while the camera is already that entity; a cut (the other id) switches.
execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1]
spectate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1]
