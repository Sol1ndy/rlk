# @s = the body: her next glide step would come nearer than 1.6 b to the avatar. A probe walks from her toward that
# step's end (#bx_nx / #bx_nz, at her height) in 0.2-b steps while the next point keeps 1.6 b from the avatar (on
# the floor plane); she glides there instead, and to the glide's end height, in the ticks the glide had left.
kill @e[type=minecraft:marker,tag=rlk_hr_bxn]
kill @e[type=minecraft:marker,tag=rlk_hr_bxp]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_bxn","rlk_room","rlk_mb_aux"]}
summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_bxp","rlk_room","rlk_mb_aux"]}
execute store result entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[0] double 0.001 run scoreboard players get #bx_nx hr
execute store result entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[2] double 0.001 run scoreboard players get #bx_nz hr
execute as @e[type=minecraft:marker,tag=rlk_hr_bxp,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
scoreboard players set #bx_k hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_bxp,limit=1] at @s run function rlk:boss/scarlet/core/guard_step
execute store result entity @e[type=minecraft:marker,tag=rlk_hr_bxp,limit=1] Pos[1] double 0.001 run scoreboard players get @s mbMvY1
scoreboard players operation #bx_k hr = @s mbMvN
scoreboard players operation #bx_k hr -= @s mbMvT
execute if score #bx_k hr matches ..0 run scoreboard players set #bx_k hr 1
execute store result storage rlk:hr bx.t int 1 run scoreboard players get #bx_k hr
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_bxp,limit=1] run function rlk:mboss/mv/glide with storage rlk:hr bx
kill @e[type=minecraft:marker,tag=rlk_hr_bxn]
kill @e[type=minecraft:marker,tag=rlk_hr_bxp]
