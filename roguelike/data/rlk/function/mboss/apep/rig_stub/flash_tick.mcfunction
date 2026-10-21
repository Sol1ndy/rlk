scoreboard players remove @s apRigF 1
execute if score @s apRigF matches ..0 as @e[type=minecraft:item_display,tag=rlk_mb_aps] run data merge entity @s {Glowing:0b}
execute if score @s apRigF matches ..0 if score @s apRigGlow matches 1 run function rlk:mboss/apep/rig_stub/look/core_glow/lit
