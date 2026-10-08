scoreboard players remove @s clNV 1
execute if score @s clNV matches 1.. run scoreboard players set #clShoot tmp 1
scoreboard players operation #lp tmp = @s clNV
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 밤순찰 stacks = #lp tmp
scoreboard players display name 밤순찰 stacks {text:"밤 순찰",color:"#C58BFF"}
execute if score @s clNV matches 0 run scoreboard players reset 밤순찰 stacks
execute if score @s clNV matches 0 run playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 0.5 1.9
scoreboard players operation #lp tmp = @s clNV
scoreboard players operation #lp tmp %= #st4 tmp
execute if score #lp tmp matches 0 run particle minecraft:electric_spark ~ ~0.9 ~ 0.3 0.5 0.3 0.05 1
# 밤 순찰 중: 1초마다 약한 스파크 소리
scoreboard players operation #lp tmp = @s clNV
scoreboard players operation #lp tmp %= #st20 tmp
execute if score #lp tmp matches 10 run playsound minecraft:block.redstone_torch.burnout master @a ~ ~ ~ 0.15 2.0
