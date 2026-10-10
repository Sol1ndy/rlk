tag @s add rlk_ohov_on
scoreboard players operation #g tmp = @s ogid
execute as @e[tag=rlk_ohint] if score @s ogid = #g tmp run data modify entity @s text set value {text:"▶ 좌클릭",color:"yellow"}
execute at @s unless score #k16 snd matches 1 run function rlk:snd/f16
