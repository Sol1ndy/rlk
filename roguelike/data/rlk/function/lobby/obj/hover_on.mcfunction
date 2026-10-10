tag @s add rlk_lhov_on
scoreboard players operation #g lob = @s lgid
execute as @e[tag=rlk_lhint] if score @s lgid = #g lob run data modify entity @s text set value {text:"▶ 좌클릭",color:"yellow"}
execute as @e[tag=rlk_lplate] if score @s lgid = #g lob run data modify entity @s block_state set value "minecraft:light_blue_concrete"
execute at @s unless score #k75 snd matches 1 run function rlk:snd/f80
