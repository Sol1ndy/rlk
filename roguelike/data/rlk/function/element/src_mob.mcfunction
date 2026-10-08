# 반응의 출처 = 몹의 공격 (@s = 맞은 플레이어). 반응 기준 #rBase = 받은 피해(#dmgIn) × #rxPlayerPct%, 원소 마스터리 없음
scoreboard players operation #rBase tmp = #dmgIn tmp
scoreboard players operation #rBase tmp *= #rxPlayerPct tmp
scoreboard players operation #rBase tmp /= #100 tmp
execute if score #rBase tmp matches ..0 run scoreboard players set #rBase tmp 1
scoreboard players set #emT tmp 0
scoreboard players set #emA tmp 0
scoreboard players set #emC tmp 0
scoreboard players set #emD tmp 0
