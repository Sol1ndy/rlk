# 신벌 (@s = 플레이어, at 몸): 하늘의 붉은 눈 → 핏빛 검기 3줄기(0 / 0.35 / 0.65초) → 잔향 전부를 소모 없이 재연(0.85초)
kill @e[tag=rlk_rnq]
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rnq"]}
execute rotated ~ 0 run tp @e[tag=rlk_rnq] ~ ~ ~ ~ 0
scoreboard players set @s rnQ 1
execute at @e[tag=rlk_rnq,limit=1] rotated as @e[tag=rlk_rnq,limit=1] run function rlk:char/ronova/burst_fx
execute at @e[tag=rlk_rnq,limit=1] rotated as @e[tag=rlk_rnq,limit=1] run function rlk:char/ronova/wave {c:130,e:20}
