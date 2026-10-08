# 몹의 1레벨 체력을 직접 지정 (@s = 몹). 사용: execute as <몹> run function rlk:mob/hp {hp:5000}   — 1024 를 넘어도 됨. 레벨 보정은 그 위에 곱해짐
$scoreboard players set @s mhp0 $(hp)
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/level_apply
