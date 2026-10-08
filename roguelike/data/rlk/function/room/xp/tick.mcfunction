# @s = 경험치 샘, at @s. 2틱마다 한 덩이씩
scoreboard players add @s life 1
execute unless score @s life matches 2.. run return 0
scoreboard players set @s life 0
execute unless score @s xpLeft matches 1.. run return run tag @s remove rlk_xpsrc
scoreboard players operation #xpAdd tmp = @s xpPulse
execute if score #xpAdd tmp > @s xpLeft run scoreboard players operation #xpAdd tmp = @s xpLeft
scoreboard players operation @s xpLeft -= #xpAdd tmp
execute as @a[tag=player,limit=1] run function rlk:player/level/add_xp
# 보이는 경험치 구슬(값 0, 연출용)
execute store result storage rlk:room o.x double 0.01 run random value -22..22
execute store result storage rlk:room o.z double 0.01 run random value -22..22
function rlk:room/xp/orb with storage rlk:room o
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 0.35 0.9
particle minecraft:happy_villager ~ ~1.2 ~ 0.3 0.3 0.3 0 2
