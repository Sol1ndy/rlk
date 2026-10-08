# 감전 틱 (@s, 물+번개가 함께 붙어 있는 동안): 1초마다 번개 피해 + 양쪽 0.4U 소모
scoreboard players add @s ecI 1
execute unless score @s ecI matches 20.. run return 0
# 감전이 끝나면 달 감전 표시도 끝
scoreboard players set @s ecI 0
scoreboard players remove @s aWater 400
scoreboard players remove @s aThunder 400
execute if score @s aWater matches ..-1 run scoreboard players set @s aWater 0
execute if score @s aThunder matches ..-1 run scoreboard players set @s aThunder 0
particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 20
playsound minecraft:entity.bee.sting master @a ~ ~ ~ 0.5 1.8
execute if score @s lnEC matches 1 run return run function rlk:element/lunar/ec_hit
scoreboard players operation #dmg tmp = @s ecDmg
scoreboard players set #elem tmp 3
function rlk:element/dot
