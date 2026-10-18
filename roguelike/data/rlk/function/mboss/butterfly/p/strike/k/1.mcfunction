# strike clock 1
function rlk:mboss/butterfly/wx/u/toward {d:0.15}
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
# the aim lock: L on the floor under the player (walk disc), her yaw S -> L, the swoop end H
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p11l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p11s]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p11h]
function rlk:mboss/butterfly/rig/face/player
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p11l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p11l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p11l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p11l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p11","rlk_mb_bf_p11s","rlk_mb_bf_kept"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] positioned ^-1.2 ^ ^2.0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p11","rlk_mb_bf_p11h","rlk_mb_bf_kept"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p11h,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_b
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] run function rlk:mboss/hz/line {len:100,w:35,tell:10,dmg:70}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] run function rlk:mboss/butterfly/fx/tele/line {len:100,w:35,back:0,tell:10,el:7,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/hz/sector {r:40,a:60,tell:10,dmg:70}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/tele/sector {r:40,a:60,tell:10,el:7,hold:3}
# the Dendro tell cue
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
