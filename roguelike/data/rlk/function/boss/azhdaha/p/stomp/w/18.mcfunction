# stomp w #azPT 18
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p5w1] run function rlk:mboss/hz/resize {r:35,r0:15,w:0}
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/cracks/1 {r:45}
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/cracks/2 {r:45}
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/cracks/3 {r:45}
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/cracks/4 {r:45}
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/cracks/5 {r:45}
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p5w2]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 13
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:15,tell:14,dmg:36}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5w2
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p5w2,limit=1] mb 2000
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5h
scoreboard players operation #aq5G2 mb = #mbGrp mb
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/crown/1
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/crown/2
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/crown/3
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/crown/4
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/crown/5
