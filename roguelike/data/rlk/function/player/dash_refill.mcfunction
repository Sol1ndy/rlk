# 대쉬 1개 충전 완료 (@s = 플레이어)
scoreboard players add @s dashCharge 1
scoreboard players set @s dashRegen 0
execute at @s unless score #k166 snd matches 1 run function rlk:snd/f229
