# @s = 평타 구체, at @s. 새로 가까워진 적으로 대상을 바꾸지 않는다.
tag @e[tag=rlk_rn_seek] remove rlk_rn_seek
scoreboard players operation #rnSeekTg tmp = @s rnTg
execute as @e[tag=rlk_mob,distance=..16] if score @s rnId = #rnSeekTg tmp run tag @s add rlk_rn_seek
execute unless entity @e[tag=rlk_rn_seek,limit=1] run return 0
# 첫 틱은 정확한 조준 방향을 유지하고, 이후 선택한 적의 이동만 기존 구체처럼 완만히 따라간다.
execute positioned ^ ^ ^2 facing entity @e[tag=rlk_rn_seek,limit=1] eyes positioned ^ ^ ^1.2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rn_guide"]}
execute at @s facing entity @e[tag=rlk_rn_guide,limit=1] feet run tp @s ~ ~ ~ ~ ~
kill @e[tag=rlk_rn_guide]
tag @e[tag=rlk_rn_seek] remove rlk_rn_seek
