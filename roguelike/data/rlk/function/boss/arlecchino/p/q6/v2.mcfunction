# Q6 volley 2 (@s = body): the landing spot = the player's floor spot now; one feather from her legs flies there
# in 14 t (glide, facing its flight); its disc(1.6) T1 plain Pyro strikes when it lands (quiet hazard).
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_fl","rlk_kn_fl2"]}
function rlk:boss/arlecchino/rig_stub/anchor/spine
execute if entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_fth","rlk_kn_fth2","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:red_dye",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.3f,1.3f,1.3f]}}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @s run summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_fth","rlk_kn_fth2","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:red_dye",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.3f,1.3f,1.3f]}}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_fl2,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] positioned as @e[type=minecraft:marker,tag=rlk_kn_fl2,limit=1] positioned ~ ~0.3 ~ run function rlk:mboss/mv/glide {t:14}
tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_kn_fl2,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:16,tell:14,dmg:38}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/q6
execute at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 0.5 1.5 0.17
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.3 1.8 0.1
