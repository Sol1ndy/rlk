scoreboard players remove @s pmAcc 100
scoreboard players add @s pmTick 1
execute if score @s pmTick > @s pmLen if data storage rlk:player_motion active{loop:1b} run scoreboard players set @s pmTick 0
execute if score @s pmTick > @s pmLen run return run function rlk:char/motion/finish
function rlk:char/motion/apply with storage rlk:player_motion active
execute if score @s pmActive matches 1 if score @s pmAcc matches 100.. run function rlk:char/motion/advance
