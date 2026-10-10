tag @s remove rlk_lhov_on
scoreboard players operation #g lob = @s lgid
execute as @e[tag=rlk_lhint] if score @s lgid = #g lob run data modify entity @s text set value {text:""}
execute as @e[tag=rlk_lplate] if score @s lgid = #g lob run data modify entity @s block_state set value "minecraft:polished_deepslate"
