# 심연의 탄환 발사 (@s = 플레이어, 위치 = 몸). 2틱마다 한 발씩, 가장 가까운 적(16칸)에게. 적이 없으면 기다림
scoreboard players add #aqT eng 1
execute if score #aqT eng matches ..1 run return 0
execute unless entity @e[tag=rlk_mob,distance=..16,limit=1] run return 0
scoreboard players set #aqT eng 0
# 다음에 쏠 원소(불 → 물 → 번개 → 얼음 → 바위 → 바람 → 풀 순)를 고르고 그 대기열을 1 줄임
scoreboard players set #aqE eng 0
execute if score #aqE eng matches 0 if score #aq1 eng matches 1.. run scoreboard players set #aqE eng 1
execute if score #aqE eng matches 0 if score #aq2 eng matches 1.. run scoreboard players set #aqE eng 2
execute if score #aqE eng matches 0 if score #aq3 eng matches 1.. run scoreboard players set #aqE eng 3
execute if score #aqE eng matches 0 if score #aq4 eng matches 1.. run scoreboard players set #aqE eng 4
execute if score #aqE eng matches 0 if score #aq5 eng matches 1.. run scoreboard players set #aqE eng 5
execute if score #aqE eng matches 0 if score #aq6 eng matches 1.. run scoreboard players set #aqE eng 6
execute if score #aqE eng matches 0 if score #aq7 eng matches 1.. run scoreboard players set #aqE eng 7
execute if score #aqE eng matches 0 run return run scoreboard players set #aqN eng 0
execute if score #aqE eng matches 1 run scoreboard players remove #aq1 eng 1
execute if score #aqE eng matches 2 run scoreboard players remove #aq2 eng 1
execute if score #aqE eng matches 3 run scoreboard players remove #aq3 eng 1
execute if score #aqE eng matches 4 run scoreboard players remove #aq4 eng 1
execute if score #aqE eng matches 5 run scoreboard players remove #aq5 eng 1
execute if score #aqE eng matches 6 run scoreboard players remove #aq6 eng 1
execute if score #aqE eng matches 7 run scoreboard players remove #aq7 eng 1
scoreboard players remove #aqN eng 1
# 피해 = 공격력의 50퍼센트 (치명타 판정 있음, 스킬 피해로 치지 않음)
function rlk:char/dmg_calc {coef:50}
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players operation #elem tmp = #aqE eng
scoreboard players set #elU tmp 1000
scoreboard players set #abyssHit tmp 1
tag @e[tag=rlk_mob,distance=..16,sort=nearest,limit=1] add rlk_abt
scoreboard players set #bi eng 0
execute positioned ~ ~1.62 ~ positioned ^ ^ ^0.6 facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:engravings/abyss/beam
execute unless score #k212 snd matches 1 run function rlk:snd/f235
execute as @e[tag=rlk_abt,limit=1] at @s run function rlk:combat/apply
tag @e[tag=rlk_abt] remove rlk_abt
scoreboard players set #abyssHit tmp 0
function rlk:char/after_hit
