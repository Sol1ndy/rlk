# event: the timeline at #sq 4 (@s = the body).
execute if score #hrEv hr matches 1 unless entity @a[tag=player,tag=rlk_mb_camh] run function rlk:boss/scarlet/fx/hud/line {id:24}
execute if score #hrEv hr matches 1 run data modify storage rlk:mboss camtx.line set value {text:{text:"조심",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 1 run function rlk:mboss/cam/text
execute if score #hrEv hr matches 1 if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #hrEv hr matches 2 unless entity @a[tag=player,tag=rlk_mb_camh] run function rlk:boss/scarlet/fx/hud/line {id:25}
execute if score #hrEv hr matches 2 run data modify storage rlk:mboss camtx.line set value {text:{text:"한잔",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 2 run function rlk:mboss/cam/text
execute if score #hrEv hr matches 2 if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
