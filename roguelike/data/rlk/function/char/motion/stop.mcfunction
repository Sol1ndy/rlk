# Hard cleanup for lifecycle changes; normal animation endings use finish.
function rlk:char/motion/release
kill @e[tag=rlk_pm]
scoreboard players set @s pmVisible 0
scoreboard players set @s pmPosValid 0
scoreboard players set @s pmBlend 0
scoreboard players set @s pmLocT 0
scoreboard players set @s pmLocAcc 0
scoreboard players set @s pmLocMode -1
scoreboard players set @s pmWeapon -1
execute if entity @e[tag=rlk_av,limit=1] run effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility
execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/av_unwrap
execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
