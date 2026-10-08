tag @s add rlk_ohov_on
scoreboard players operation #g tmp = @s ogid
execute as @e[tag=rlk_ohint] if score @s ogid = #g tmp run data modify entity @s text set value {text:"▶ 좌클릭",color:"yellow"}
execute at @s run playsound minecraft:block.note_block.hat master @a ~ ~ ~ 0.6 1.9
