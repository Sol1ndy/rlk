scoreboard players remove @s fgRigY 1
execute if score @s fgRigY matches ..0 as @e[type=minecraft:item_display,tag=rlk_mb_fgs] run data merge entity @s {Glowing:0b}
