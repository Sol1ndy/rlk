# @s = 공격자/투사체. 근접은 공격자 반대 방향, 포탄은 폭발 중심 반대 방향.
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb_source"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
# 화살·화염구는 몸 중심을 지나친 뒤에도 진행 방향으로 민다.
execute if entity @s[tag=rlk_cmp_ar] at @e[tag=rlk_body,limit=1] rotated as @s run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
execute if entity @s[tag=rlk_cmp_fb] at @e[tag=rlk_body,limit=1] rotated as @s run tp @e[tag=rlk_plkb_source,limit=1] ~ ~ ~ ~ 0
