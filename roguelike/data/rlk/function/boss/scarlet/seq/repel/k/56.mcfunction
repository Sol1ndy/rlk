# repel: the timeline at #sq 56 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.2 ^1 run function rlk:boss/scarlet/fx/p/qi_arc {r:22,yaw:0,pitch:0,roll:40,c:5}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.2 ^1 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
function rlk:boss/scarlet/seq/repel/m/stagger
