# @s = 플레이어 (player/def/dg_refund: 이번 닷지 도장이 처음으로 공격을 피했다 — 퍼펙트 · 넓은 닷지, 홍련 조각의 퍼펙트 창 물음; 도장
# 하나에 한 번). 원작처럼 그 순간 공격한 적(rlk_hc_atk; 없으면 몸이 보는 반대쪽)에게서 똑바로 물러서는 백스텝으로 바꾼다: 방향 =
# 적 → 몸(수평), 4틱 2.7칸(player/dodge/speed4). 더블 닷지의 옆돌기는 동작은 그대로 두고 방향만 물러서는 쪽으로. 아바타: 리그 캐릭터는
# 클립 dash_b(적을 보며 뒤로; 퍼펙트 닷지의 백 핸드스프링 · 옆돌기를 덮지 않음), 마네킹 캐릭터는 웅크림
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #cx tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #cz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_hc_atk,limit=1] feet rotated ~180 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~180 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute store result score #vx tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[0] 100
execute store result score #vz tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
scoreboard players operation #vx tmp -= #cx tmp
scoreboard players operation #vz tmp -= #cz tmp
function rlk:player/dash_norm
scoreboard players operation @s dashDX = #ux tmp
scoreboard players operation @s dashDX *= #st10 tmp
scoreboard players operation @s dashDZ = #uz tmp
scoreboard players operation @s dashDZ *= #st10 tmp
scoreboard players operation @s dashUX = #ux tmp
scoreboard players operation @s dashUZ = #uz tmp
# 옆돌기 중이면 방향만(남은 이동 틱 그대로)
execute if score #dgMv cb matches 2 if score @s dashMoveT matches 1.. run return 0
scoreboard players set #dgMv cb 4
function rlk:player/dodge/len
execute if score @s pmActive matches 1 unless data storage rlk:player_motion active{clip:"dash"} unless data storage rlk:player_motion active{clip:"dash_l"} unless data storage rlk:player_motion active{clip:"dash_b"} run return 0
execute if score #btK cb matches 2 if score #btA cb matches 0 run return 0
function rlk:char/motion/dash_b
