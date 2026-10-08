# 체력 스코어가 없는 몹의 첫 준비 (@s = 몹): 1레벨 체력(mhp0) = 지금의 바닐라 최대 체력, 레벨이 없으면 1
execute unless score @s mhp0 matches 1.. store result score @s mhp0 run attribute @s minecraft:max_health base get
execute unless score @s mhp0 matches 1.. run scoreboard players set @s mhp0 1
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/level_apply
