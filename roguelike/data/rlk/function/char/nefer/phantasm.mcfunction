# 환영극 (@s = 플레이어, at 몸): 풀 이슬 1개 소모. 네페르 2타 + 그림자 3타 — 탁(네페르) · 타(네페르 + 그림자) · 닥(그림자) · 탁(그림자)
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
execute if score @s nfPT matches 1.. run return 0
scoreboard players remove @s nfDew 1
scoreboard players add @s nfPh 1
scoreboard players set @s nfPT 1
scoreboard players set @s atkCD 20
scoreboard players set @s comboStep 0
# 그림자가 나타날 자리: 조준한 전방 적(8칸) → 전방 5칸의 가장 가까운 적 → 앞으로 2칸
tag @e[tag=rlk_nftg] remove rlk_nftg
function rlk:combat/melee_begin
execute positioned ~ ~1.62 ~ positioned ^ ^ ^ run function rlk:char/nefer/find
execute as @e[tag=rlk_nftg,limit=1] run function rlk:combat/melee_front
execute if score #meleeFront tmp matches 0 run tag @e[tag=rlk_nftg] remove rlk_nftg
execute unless entity @e[tag=rlk_nftg,limit=1] as @e[tag=rlk_mob,distance=..5,sort=nearest] run function rlk:char/nefer/ph_front_target
kill @e[tag=rlk_melee_origin]
kill @e[tag=rlk_nfsp]
execute if entity @e[tag=rlk_nftg,limit=1] as @e[tag=rlk_nftg,limit=1] at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nfsp"]}
execute unless entity @e[tag=rlk_nfsp,limit=1] rotated ~ 0 positioned ^ ^ ^2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nfsp"]}
execute as @e[tag=rlk_nfsp] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
tag @e[tag=rlk_nftg] remove rlk_nftg
# 달빛 승부사: 주변 8칸의 기만의 핵을 흡수 → 기만의 장막
execute as @e[tag=rlk_dcore,distance=..8] run function rlk:char/nefer/dec_absorb
# 그림자 소환(노리는 자리 건너편에서 그 자리를 바라봄)
function rlk:char/nefer/shadow_spawn
execute unless score #k269 snd matches 1 run function rlk:snd/f397
execute unless score #k312 snd matches 1 run function rlk:snd/f359
execute unless score #k337 snd matches 1 run function rlk:snd/f398
# 그림자 춤 끝: 환영극 3번
execute if score @s nfPh matches 3.. run scoreboard players set @s nfSD 0
scoreboard players set #basic itv 1
function rlk:items/hook/on_basic_attack
scoreboard players set #basic itv 0
