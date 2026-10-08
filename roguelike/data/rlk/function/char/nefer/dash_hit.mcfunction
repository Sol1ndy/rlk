# 돌진 피해 (@s = 플레이어): 공격력 76% + 원소 마스터리 46%, 풀 원소(2U) · 원소전투 스킬 피해. 원소 입자 3개
execute at @e[tag=rlk_body,limit=1] run tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
function rlk:char/nefer/calc {a:76,e:46}
scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 2000
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
execute as @e[tag=rlk_hit] at @s run particle minecraft:composter ~ ~1 ~ 0.3 0.5 0.3 0 10
tag @e[tag=rlk_hit] remove rlk_hit
execute if score #hitLanded tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:char/particles {n:3,el:7}
execute at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
