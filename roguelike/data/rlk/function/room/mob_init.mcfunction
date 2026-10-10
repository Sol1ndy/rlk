# @s = 방금 소환된 몹: 종류별 1레벨 체력/공격력/경험치 + 레벨
execute if entity @s[tag=rlk_m_husk] run scoreboard players set #mhp tmp 16
execute if entity @s[tag=rlk_m_husk] run scoreboard players set #mad tmp 3
execute if entity @s[tag=rlk_m_husk] run scoreboard players set @s xpDrop 4
execute if entity @s[tag=rlk_m_skel] run scoreboard players set #mhp tmp 12
execute if entity @s[tag=rlk_m_skel] run scoreboard players set #mad tmp 2
execute if entity @s[tag=rlk_m_skel] run scoreboard players set @s xpDrop 4
execute if entity @s[tag=rlk_m_vind] run scoreboard players set #mhp tmp 26
execute if entity @s[tag=rlk_m_vind] run scoreboard players set #mad tmp 4
execute if entity @s[tag=rlk_m_vind] run scoreboard players set @s xpDrop 8
execute if entity @s[tag=rlk_m_boss] run scoreboard players set #mhp tmp 400
execute if entity @s[tag=rlk_m_boss] run scoreboard players set #mad tmp 6
execute if entity @s[tag=rlk_m_boss] run scoreboard players set @s xpDrop 40
# 1챕터 커스텀 몹(공격력 0: 모든 공격은 cm/* 함수가 직접)
execute if entity @s[tag=rlk_m_cmsw] run scoreboard players set #mhp tmp 18
execute if entity @s[tag=rlk_m_cmsw] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmsw] run scoreboard players set @s xpDrop 4
execute if entity @s[tag=rlk_m_cmar] run scoreboard players set #mhp tmp 12
execute if entity @s[tag=rlk_m_cmar] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmar] run scoreboard players set @s xpDrop 4
execute if entity @s[tag=rlk_m_cmfm] run scoreboard players set #mhp tmp 12
execute if entity @s[tag=rlk_m_cmfm] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmfm] run scoreboard players set @s xpDrop 5
execute if entity @s[tag=rlk_m_cmim] run scoreboard players set #mhp tmp 12
execute if entity @s[tag=rlk_m_cmim] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmim] run scoreboard players set @s xpDrop 5
execute if entity @s[tag=rlk_m_cmsh] run scoreboard players set #mhp tmp 20
execute if entity @s[tag=rlk_m_cmsh] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmsh] run scoreboard players set @s xpDrop 8
execute if entity @s[tag=rlk_m_cmcn] run scoreboard players set #mhp tmp 16
execute if entity @s[tag=rlk_m_cmcn] run scoreboard players set #mad tmp 0
execute if entity @s[tag=rlk_m_cmcn] run scoreboard players set @s xpDrop 6
# 레벨 = (챕터 - 1) × 6 + 이번 맵의 순서(1~6). 체력은 레벨에 따라 늘어남(mob/level_apply), 공격력은 맞을 때 레벨로 보정
scoreboard players operation @s mlv = #chapter room
scoreboard players remove @s mlv 1
scoreboard players operation @s mlv *= #st6 tmp
scoreboard players operation @s mlv += #mapIdx room
scoreboard players add @s mlv 1
scoreboard players operation @s mhp0 = #mhp tmp
execute store result storage rlk:room m.hp int 1 run scoreboard players get #mhp tmp
execute store result storage rlk:room m.ad int 1 run scoreboard players get #mad tmp
function rlk:room/mob_init2 with storage rlk:room m
function rlk:mob/level_apply
attribute @s minecraft:follow_range base set 128
tag @s remove rlk_newmob
