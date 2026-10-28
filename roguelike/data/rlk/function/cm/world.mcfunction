# 커스텀 몹이 있을 때 매 틱
execute unless entity @e[tag=rlk_body,limit=1] run return 0
# 조준점(몸 가슴) · 방향 계산용 표식 · 미끼(바닐라 근접 공격을 대신 맞는 투명 마네킹)
execute unless entity @e[tag=rlk_cmaim,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_cmaim","rlk_cmglob"]}
execute unless entity @e[tag=rlk_cmrot,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_cmrot","rlk_cmglob"]}
execute unless entity @e[tag=rlk_lure,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:cm/lure_new
execute at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_cmaim] ~ ~1.1 ~
execute at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_lure] ~ ~ ~
data modify entity @e[tag=rlk_lure,limit=1] Health set value 1024f
# 로노바가 쓰러져 있으면 아무것도 하지 않음
scoreboard players set #cmDown tmp 0
execute if entity @a[tag=player,scores={rnDie=1..}] run scoreboard players set #cmDown tmp 1
execute if entity @e[tag=rlk_c2,limit=1] run function rlk:cm/c2/world
execute as @e[tag=rlk_cmb] at @s run function rlk:cm/tick
