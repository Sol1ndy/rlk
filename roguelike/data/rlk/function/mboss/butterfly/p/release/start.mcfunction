# B5 달빛 해제 (STUB; clip release: dome telegraph 38, detonation 53).
function rlk:mboss/butterfly/rig_stub/face/player
function rlk:mboss/butterfly/u/lockp
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p15a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p15a] remove rlk_mb_bf_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15a,limit=1] facing entity @s feet rotated ~180 0 positioned ^ ^ ^3 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p15b"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p15b,limit=1] run function rlk:mboss/mv/clamp
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p15b,limit=1] run function rlk:mboss/mv/glide {t:14}
playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
