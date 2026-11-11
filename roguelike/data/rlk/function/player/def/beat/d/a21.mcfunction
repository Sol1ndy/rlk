# 21틱: 착지. 붉은 기운이 걷힘, 가벼운 착지 소리 · 먼지
execute as @a[tag=player,limit=1] run function rlk:char/motion/beat/tint_off
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.wool.fall player @a[tag=player] ~ ~ ~ 0.9 0.8
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cloud ~ ~0.1 ~ 0.25 0.02 0.25 0.01 4 normal @a[tag=player]
