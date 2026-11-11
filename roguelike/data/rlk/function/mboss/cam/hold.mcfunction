# FN-cam, from rlk:tick right after mboss/main while #mbCam mb is 1 (@s = the tagged player): the player watches the
# live camera stand (#mbCamId mb 1 = rlk_mb_cam1, 2 = rlk_mb_cam2) in spectator mode. `spectate` is issued every tick (it
# sends nothing while the camera is already that stand); while Shift is held the player is snapped to the stand instead.
# No fight any more (the request outlived it): the request is dropped and the player released.
execute unless score #mbLive mb matches 1 run scoreboard players set #mbCam mb 0
execute unless score #mbLive mb matches 1 run return run function rlk:mboss/cam/release
# The player is their own body (developer mode; the tick after a relog or a /reload rebuilt the view: no avatar to
# leave behind): never locked, and a player who still carries the hold from before is released.
execute if entity @s[tag=rlk_body] run return run function rlk:mboss/cam/release
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:mboss/cam/release
# The live stand is gone (killed): the player is not left a free spectator; the lock comes back with the stand.
execute if score #mbCamId mb matches 2 unless entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run return run function rlk:mboss/cam/release
execute unless score #mbCamId mb matches 2 unless entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run return run function rlk:mboss/cam/release
execute unless entity @s[tag=rlk_mb_camh] run function rlk:mboss/cam/hold_in
# Shift held (HF-B, HB-02): the game ends the spectating after this function every tick (ServerPlayer.tick:
# wantsToStopRiding -> setCamera(self)), so a re-issued spectate is undone in the same tick and the player keeps their own
# spectator view there. Instead the player is put at the live stand's eye with its rotation (a teleport ends a spectate:
# nothing else runs): the view the client is snapped back to every tick is the shot's. Holding Shift loosens the view
# between those snaps (the mouse turns it, Shift sinks it) until it is released; the next tick spectates again.
execute if predicate rlk:in_sneak if score #mbCamId mb matches 2 at @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] rotated as @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run return run tp @s ~ ~-0.10125 ~ ~ ~
execute if predicate rlk:in_sneak unless score #mbCamId mb matches 2 at @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] rotated as @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run return run tp @s ~ ~-0.10125 ~ ~ ~
execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1]
spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1]
