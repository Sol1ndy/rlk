# 몬스터 레벨 지정 (@s = 몹). 사용: execute as <몹> run function rlk:mob/level {lv:5}
# 체력 = 1레벨 체력 × (100 + #mobLvHp × (레벨 - 1))% (상한 없음. 1레벨 체력을 직접 정하려면 mob/hp). 공격력은 맞을 때 레벨로 보정(player/take_damage)
$scoreboard players set @s mlv $(lv)
execute unless score @s mhp0 matches 1.. store result score @s mhp0 run attribute @s minecraft:max_health base get
function rlk:mob/level_apply
