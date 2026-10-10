# 빙참 (공허+얼음): 얼음 파편 5개가 튀어 나가 주변 적(6칸, 가까운 순)에게 꽂힌다. 남는 파편은 휘어서 대상에게. 파편마다 얼음 피해 80% + 잠식 +5%
function rlk:element/calc {m:80}
scoreboard players set @s rxQ 20
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 4
