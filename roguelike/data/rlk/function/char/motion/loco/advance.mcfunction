scoreboard players remove @s pmLocAcc 100
scoreboard players add @s pmLocT 1
function rlk:char/motion/loco/frame with storage rlk:player_motion loco
execute if score @s pmLocAcc matches 100.. run function rlk:char/motion/loco/advance
