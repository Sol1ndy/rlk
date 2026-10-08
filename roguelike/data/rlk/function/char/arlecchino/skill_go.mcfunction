# 다시 나타남 (@s = 플레이어): 대상이 있으면 그 앞으로 → 그 자리에서 벤다
execute if entity @e[tag=rlk_artg,limit=1] run function rlk:char/arlecchino/skill_dash
tag @e[tag=rlk_artg] remove rlk_artg
execute at @e[tag=rlk_body,limit=1] run function rlk:char/arlecchino/skill_hit
