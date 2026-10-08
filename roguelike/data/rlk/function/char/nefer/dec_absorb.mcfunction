# 기만의 핵 흡수 (@s = 기만의 핵): 플레이어 쪽으로 빛줄기 + 기만의 장막 +1(최대 3), 8초
execute at @s run particle minecraft:dust{color:[0.75,0.95,0.6],scale:1.2} ~ ~0.3 ~ 0.2 0.2 0.2 0 10
execute as @a[tag=player,limit=1] run function rlk:char/nefer/veil_add
kill @s
