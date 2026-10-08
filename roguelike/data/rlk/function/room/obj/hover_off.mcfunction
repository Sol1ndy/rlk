tag @s remove rlk_ohov_on
scoreboard players operation #g tmp = @s ogid
execute as @e[tag=rlk_ohint] if score @s ogid = #g tmp run data modify entity @s text set value {text:""}
