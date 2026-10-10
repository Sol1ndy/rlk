# 연소 틱 (@s): 풀 부착을 초당 0.4U 씩 태우며 0.5초마다 불 피해. 풀이나 불이 사라지면 끝
execute unless score @s aGrass matches 1.. run return run scoreboard players set @s burnOn 0
execute unless score @s aFire matches 1.. run return run scoreboard players set @s burnOn 0
scoreboard players remove @s aGrass 20
execute if score @s aGrass matches ..-1 run scoreboard players set @s aGrass 0
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.01 1
scoreboard players add @s burnI 1
execute unless score @s burnI matches 10.. run return 0
scoreboard players set @s burnI 0
# 타는 동안 불 부착 유지
execute unless score @s aFire matches 800.. run scoreboard players set @s aFire 800
execute unless score #k40 snd matches 1 run function rlk:snd/f42
scoreboard players operation #dmg tmp = @s burnDmg
scoreboard players set #elem tmp 1
function rlk:element/dot
