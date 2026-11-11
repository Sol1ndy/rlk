# A8 pattern tick 220.
kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute as @e[type=minecraft:item_display,tag=rlk_hr_swl] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
function rlk:boss/scarlet/shield/judge
function rlk:boss/scarlet/fx/hud/warn {on:0}
execute if score #gres hr matches 2 run function rlk:boss/scarlet/p/a8/fail
execute if score #gres hr matches 1 run scoreboard players set #done hr 1
