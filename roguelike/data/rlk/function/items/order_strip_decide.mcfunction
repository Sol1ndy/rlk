# 현재 원소 scur 가 제거 대상(t1)이고 남은 제거 수(#n1)가 있으면 스킵, 아니면 order 에 유지
scoreboard players set #skip tmp 0
$execute if data storage rlk:pinv {t1:"$(scur)"} if score #n1 tmp matches 1.. run scoreboard players set #skip tmp 1
execute if score #skip tmp matches 1 run scoreboard players remove #n1 tmp 1
execute if score #skip tmp matches 0 run data modify storage rlk:pinv order append from storage rlk:pinv scur
