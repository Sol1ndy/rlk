# 몬스터 레벨 지정 (@s = 몹). 사용: execute as <몹> run function rlk:mob/level {lv:5}
# 체력·공격·방어의 레벨 보정은 load 의 #mobLv* 상수 참고(mob/level_apply, player/hurt_lv, combat/lv_mult). 1레벨 체력을 직접 정하려면 mob/hp
$scoreboard players set @s mlv $(lv)
execute unless score @s mhp0 matches 1.. store result score @s mhp0 run attribute @s minecraft:max_health base get
function rlk:mob/level_apply
