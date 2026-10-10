# 같은 원소: 막을 수 있는 양 = 방어막 × 250%, 방어막은 막은 양 ÷ 2.5 만큼(올림) 줄어든다
scoreboard players operation #cap tmp = @s shieldHP
scoreboard players operation #cap tmp *= #shElEff tmp
scoreboard players operation #cap tmp /= #100 tmp
scoreboard players operation #ab tmp = #cap tmp
execute if score #dmgIn tmp < #ab tmp run scoreboard players operation #ab tmp = #dmgIn tmp
scoreboard players operation #cost tmp = #ab tmp
scoreboard players operation #cost tmp *= #100 tmp
scoreboard players operation #cost tmp += #shElEff tmp
scoreboard players remove #cost tmp 1
scoreboard players operation #cost tmp /= #shElEff tmp
scoreboard players operation @s shieldHP -= #cost tmp
execute if score @s shieldHP matches ..0 run scoreboard players set @s shieldHP 0
scoreboard players operation #dmgIn tmp -= #ab tmp
execute at @s unless score #k41 snd matches 1 run function rlk:snd/f43
execute at @s unless score #k42 snd matches 1 run function rlk:snd/f44
execute unless score @s shieldHP matches 1.. run scoreboard players set @s shieldT 0
