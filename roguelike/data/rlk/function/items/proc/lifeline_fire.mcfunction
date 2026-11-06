# @s = 플레이어, 위치 = 몸. 대쉬가 끝남: 실이 감긴 모든 적에게 최대 체력의 #lifelinePm‰ 물 원소 피해 (강화 단계로 조정)
execute at @e[tag=rlk_llm] run particle minecraft:dust{color:[0.31f,0.72f,1.0f],scale:1.1f} ~ ~1.1 ~ 0.3 0.6 0.3 0 14
execute at @e[tag=rlk_llm] run particle minecraft:splash ~ ~1 ~ 0.3 0.3 0.3 0.1 12
execute unless score #k116 snd matches 1 run function rlk:snd/f124
data modify storage rlk:tune m_lifeline.obj set value "maxHealth"
execute store result storage rlk:tune m_lifeline.pm int 1 run scoreboard players get #lifelinePm tmp
execute as @a[tag=player,limit=1] run function rlk:items/calc_stat with storage rlk:tune m_lifeline
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_llm] add rlk_hit
tag @e[tag=rlk_llm] remove rlk_llm
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
