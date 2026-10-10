# Called as the boss after a real body hit. Visual feedback only.
scoreboard players set @s rdRigHit 4
execute as @e[tag=rlk_raiden_part] run data merge entity @s {Glowing:1b,glow_color_override:13383423}
