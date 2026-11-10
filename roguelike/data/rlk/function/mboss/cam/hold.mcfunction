# FN-cam, from rlk:tick right after mboss/main while #mbCam mb is 1 (@s = the tagged player): the player watches the
# live camera stand (#mbCamId mb 1 = rlk_mb_cam1, 2 = rlk_mb_cam2) in spectator mode. `spectate` is issued every tick: a
# sneaking player leaves a spectated entity (ServerPlayer.tick), the next tick takes them back.
# No fight any more (the request outlived it): the request is dropped and the player released.
execute unless score #mbLive mb matches 1 run scoreboard players set #mbCam mb 0
execute unless score #mbLive mb matches 1 run return run function rlk:mboss/cam/release
# The player is their own body (developer mode: no avatar to leave behind): never locked.
execute if entity @s[tag=rlk_body] run return 0
execute unless entity @e[tag=rlk_av,limit=1] run return 0
# The live stand is gone (killed): the player is not left a free spectator; the lock comes back with the stand.
execute if score #mbCamId mb matches 2 unless entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] run return run function rlk:mboss/cam/release
execute unless score #mbCamId mb matches 2 unless entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] run return run function rlk:mboss/cam/release
execute unless entity @s[tag=rlk_mb_camh] run function rlk:mboss/cam/hold_in
execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1]
spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1]
