# 가까운 순서로 확인하되, 이미 전방 대상을 찾았으면 종료한다. @s = 후보 몹.
execute if entity @e[tag=rlk_nftg,limit=1] run return 0
function rlk:combat/melee_front
execute if score #meleeFront tmp matches 1 run tag @s add rlk_nftg
