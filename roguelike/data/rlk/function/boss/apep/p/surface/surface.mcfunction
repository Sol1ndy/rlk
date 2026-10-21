# @s = body (t36): the surfacing splash (impact visual), the charge; lock L at the player; the shell r
# 3.0 (tell 12, 130 %) with its keep decal (the pale disc under the player); the
# light band length (muzzle -> L) for t46.
execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/surface_splash
execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/water_splash
execute at @s run function rlk:boss/apep/fx/snd/q3s_surface
execute at @s run function rlk:boss/apep/fx/snd/q3s_charge
function rlk:boss/apep/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p36l]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p36l
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p36l] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p36l] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p36l,limit=1] run function rlk:boss/apep/p/surface/shell_hz
function rlk:boss/apep/p/surface/dist
scoreboard players remove #apq36D mb 43
execute if score #apq36D mb matches ..9 run scoreboard players set #apq36D mb 10
execute store result storage rlk:mboss ap.p36.len int 1 run scoreboard players get #apq36D mb
