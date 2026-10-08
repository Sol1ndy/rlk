# 대상 앞으로 (@s = 플레이어). 나타날 자리 표식 rlk_arto: 대상에서 몸 쪽으로 1.4칸(막혔으면 0.9칸)
kill @e[tag=rlk_arto]
execute as @e[tag=rlk_artg,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.4 if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass run summon minecraft:marker ~ ~ ~ {Tags:["rlk_arto"]}
execute unless entity @e[tag=rlk_arto,limit=1] as @e[tag=rlk_artg,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.9 if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass run summon minecraft:marker ~ ~ ~ {Tags:["rlk_arto"]}
execute unless entity @e[tag=rlk_arto,limit=1] run return 0
# 떠난 자리 · 나타난 자리 효과
execute at @e[tag=rlk_body,limit=1] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 15
execute at @e[tag=rlk_arto,limit=1] run particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.6} ~ ~1 ~ 0.3 0.6 0.3 0 20
# 숄더뷰 = 아바타를 옮기고 대상을 보게 / 1인칭 = 플레이어 자리만 옮김(시야는 그대로)
execute if entity @e[tag=rlk_av,limit=1] unless entity @s[tag=rlk_body] at @e[tag=rlk_arto,limit=1] run tp @e[tag=rlk_av,limit=1] ~ ~ ~ facing entity @e[tag=rlk_artg,limit=1] feet
execute if entity @s[tag=rlk_body] at @e[tag=rlk_arto,limit=1] run tp @s ~ ~ ~
execute as @e[tag=rlk_av,limit=1] run data modify entity @s Motion set value [0.0d,0.0d,0.0d]
kill @e[tag=rlk_arto]
