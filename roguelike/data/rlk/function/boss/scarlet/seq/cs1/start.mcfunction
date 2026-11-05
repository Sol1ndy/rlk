# CS1 (PLAN §3.2): the lunge, the blade lock, apart, the iai under the brim, the petals, 홍련일섬, the crimson field.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/rig/face/player
execute positioned as @e[tag=rlk_body,limit=1] run function rlk:mboss/pull/start {t:0}
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/cs1
scoreboard players set #sqdone hr 0
scoreboard players set @a[tag=player] hudHold 2
function rlk:boss/scarlet/seq/cs1/m/lunge
execute positioned ~ ~0 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/afterimage {len:20}
