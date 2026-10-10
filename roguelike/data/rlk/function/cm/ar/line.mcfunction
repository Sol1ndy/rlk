# 궤적 선 (@s = 선, 위치/방향 = 궁수 눈 → 조준점). 길이 = 벽까지(최대 24칸)
tp @s ~ ~ ~ ~ ~
scoreboard players set #rl tmp 0
function rlk:cm/ray
execute store result entity @s transformation.scale[2] float 0.5 run scoreboard players get #rl tmp
