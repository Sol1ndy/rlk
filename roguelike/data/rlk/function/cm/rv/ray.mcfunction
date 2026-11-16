# 0.2 b steps along the feet path; the brain's box (feet + 0.25 / 0.95 / 1.7) must stay in open air
execute if entity @e[tag=rlk_rv_tsel,distance=..0.25] run return run scoreboard players set #ok tmp 1
execute unless block ~ ~0.25 ~ #rlk:dash_pass run return 0
execute unless block ~ ~0.95 ~ #rlk:dash_pass run return 0
execute unless block ~ ~1.7 ~ #rlk:dash_pass run return 0
scoreboard players remove #n tmp 1
execute if score #n tmp matches 1.. positioned ^ ^ ^0.2 run function rlk:cm/rv/ray
