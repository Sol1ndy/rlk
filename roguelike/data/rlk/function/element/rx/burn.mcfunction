# 연소 (불+풀): 풀이 타는 동안 0.5초마다 불 피해 50% (원신의 0.25초마다 25% 와 같은 초당 피해)
function rlk:element/calc {m:50}
scoreboard players operation @s burnDmg = #rdmg tmp
execute unless score @s burnOn matches 1 run scoreboard players set #rx tmp 10
execute unless score @s burnOn matches 1 run scoreboard players set @s burnI 0
scoreboard players set @s burnOn 1
