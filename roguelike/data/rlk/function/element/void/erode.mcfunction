# 공허 공격에 맞음 (@s = 몹): 잠식 +#rnErAdd(없으면 #rnErHit)%
scoreboard players operation #g tmp = #rnErAdd tmp
execute unless score #g tmp matches 1.. run scoreboard players operation #g tmp = #rnErHit tmp
function rlk:element/void/er_add
