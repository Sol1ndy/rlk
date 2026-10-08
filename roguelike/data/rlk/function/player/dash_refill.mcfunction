# 대쉬 1개 충전 완료 (@s = 플레이어)
scoreboard players add @s dashCharge 1
scoreboard players set @s dashRegen 0
execute at @s run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 0.5 1.6
