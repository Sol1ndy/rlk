# The intro skip prompt off for good (the window ended, the skip).
scoreboard players set #sq_skd hr 1
execute as @e[type=minecraft:text_display,tag=rlk_mb_camk] run data merge entity @s {text:"",background:0}
execute unless entity @a[tag=player,tag=rlk_mb_camh] run title @a[tag=player] actionbar ""
