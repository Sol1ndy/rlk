# 3챕터 몹 공용, 매 틱 두뇌보다 먼저 (cm/world). 한 틱 피격 제한 · 같은 틱 시작 표시 · 포자 피해 표시
scoreboard players set #c3FuHit tmp 0
scoreboard players set #c3EmHit tmp 0
scoreboard players set #c3SbHit tmp 0
execute if entity @e[tag=rlk_c3fresh,limit=1] run tag @e[tag=rlk_c3fresh] remove rlk_c3fresh
execute if entity @e[tag=rlk_c3pz,limit=1] run tag @e[tag=rlk_c3pz] remove rlk_c3pz
execute unless entity @e[tag=rlk_c2vec,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2vec","rlk_cmglob"]}
