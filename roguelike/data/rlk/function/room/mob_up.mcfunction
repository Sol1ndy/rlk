# 땅 위 찾기 (위치 = 후보 칸, 바닥 바로 위부터): 막혀 있으면 한 칸씩 위로(최대 5칸). 기둥 · 나무 위는 안 됨
scoreboard players add #mu tmp 1
execute if score #mu tmp matches 7.. run return 0
execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run function rlk:room/mob_up
execute unless block ~ ~1 ~ #rlk:dash_pass run return 0
execute if block ~ ~-1 ~ #minecraft:leaves run return 0
execute if block ~ ~-1 ~ #minecraft:logs run return 0
execute if block ~ ~-1 ~ #rlk:no_spawn run return 0
# 2챕터(이나즈마, #th 4): 집 · 가게 안은 안 됨. 이 테마에서 가문비나무 판자는 집 · 가게(room/prop/i_house_* · i_shop*)의 실내 바닥에만 쓰인다
execute if score #th room matches 4 if block ~ ~-1 ~ minecraft:spruce_planks run return 0
function rlk:room/mob_summon
scoreboard players set #placed tmp 1
