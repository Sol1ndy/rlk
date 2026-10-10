# 땅 위 찾기 (위치 = 후보 칸, 바닥 바로 위부터): 막혀 있으면 한 칸씩 위로(최대 5칸). 기둥 · 나무 위는 안 됨
scoreboard players add #mu tmp 1
execute if score #mu tmp matches 7.. run return 0
execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run function rlk:room/mob_up
execute unless block ~ ~1 ~ #rlk:dash_pass run return 0
execute if block ~ ~-1 ~ #minecraft:leaves run return 0
execute if block ~ ~-1 ~ #minecraft:logs run return 0
execute if block ~ ~-1 ~ #rlk:no_spawn run return 0
function rlk:room/mob_summon
scoreboard players set #placed tmp 1
