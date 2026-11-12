# cs1: the timeline at #sq 618 (@s = the body).
execute unless entity @a[tag=player,tag=rlk_mb_camh] run function rlk:boss/scarlet/fx/hud/line {id:16}
data modify storage rlk:mboss camtx.line set value {text:{text:"이런",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.92 ^2.515 ^1.15 run tp @s ~ ~ ~
