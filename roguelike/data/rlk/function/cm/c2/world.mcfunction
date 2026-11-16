# 2챕터 몹 공용, 매 틱 두뇌보다 먼저 (cm/world). 한 틱 피격 제한 · 북 가속 표시 · 가속 기운
scoreboard players set #c2NsHit tmp 0
scoreboard players set #c2SpHit tmp 0
execute if entity @e[tag=rlk_c2fresh,limit=1] run tag @e[tag=rlk_c2fresh] remove rlk_c2fresh
scoreboard players add #c2Clk tmp 1
execute if score #c2Clk tmp matches 20.. run scoreboard players set #c2Clk tmp 0
execute unless entity @e[tag=rlk_c2vec,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2vec","rlk_cmglob"]}
# 북잡이가 북을 치는 동안 10칸 안의 모든 커스텀 몹(북잡이 제외)에 rlk_cm_haste. 매 틱 지우고 다시 붙인다
execute if entity @e[tag=rlk_cm_haste,limit=1] run tag @e[tag=rlk_cm_haste] remove rlk_cm_haste
execute as @e[tag=rlk_dr_drum] at @s run tag @e[tag=rlk_cmb,tag=!rlk_cm_dr,distance=..10] add rlk_cm_haste
scoreboard players operation #c2m tmp = #c2Clk tmp
scoreboard players operation #c2m tmp %= #c2c4 tmp
execute if score #c2m tmp matches 0 as @e[tag=rlk_cm_haste] at @s run particle minecraft:dust{color:[1.0,0.82,0.18],scale:1.2} ~ ~0.9 ~ 0.35 0.55 0.35 0 4 normal
execute if score #c2m tmp matches 2 as @e[tag=rlk_cm_haste] at @s run particle minecraft:wax_on ~ ~1.1 ~ 0.3 0.5 0.3 0 1 normal
