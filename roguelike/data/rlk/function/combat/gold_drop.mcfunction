# 로비(튜토리얼 · 체험)의 더미 · 허수아비는 주지 않음
execute if entity @s[tag=rlk_lobby] run return 0
# 처치 시 골드 드롭 (@s = 죽는 몹, at @s). 양 = 무작위(#mobGoldMin~#mobGoldMax) × 챕터, 보스(boss 태그)는 × #bossGoldMul
# 런 밖(챕터 값이 없을 때)은 × 1
execute store result score #gr tmp run random value 0..9999
scoreboard players operation #gv tmp = #mobGoldMax tmp
scoreboard players operation #gv tmp -= #mobGoldMin tmp
scoreboard players add #gv tmp 1
scoreboard players operation #gr tmp %= #gv tmp
scoreboard players operation #gv tmp = #gr tmp
scoreboard players operation #gv tmp += #mobGoldMin tmp
execute if score #active room matches 1 if score #chapter room matches 2.. run scoreboard players operation #gv tmp *= #chapter room
execute if entity @s[tag=boss] unless entity @s[tag=miniboss] run scoreboard players operation #gv tmp *= #bossGoldMul tmp
# 중간보스(boss + miniboss): 골드 × #mbGoldMul, 사파이어 조각 #mbSap (레지스트리 goldMul · sap). 챕터 보스(boss만, miniboss 없음)는 위의 보스 경제(× #bossGoldMul, #bossSapphire)
execute if entity @s[tag=rlk_mb_body,tag=miniboss] run scoreboard players operation #gv tmp *= #mbGoldMul mb
# 동전 주머니: 추가 골드(개수만큼)
scoreboard players operation #t1 itv = @a[tag=player,limit=1] it_coin_pouch
scoreboard players operation #t1 itv *= #pouchGold tmp
execute if score #t1 itv matches 1.. run scoreboard players operation #gv tmp += #t1 itv
# 보스: 사파이어 조각 (개수 = #bossSapphire)
execute if entity @s[tag=boss] unless entity @s[tag=miniboss] run scoreboard players operation #sapN tmp = #bossSapphire tmp
execute if entity @s[tag=boss] unless entity @s[tag=miniboss] run function rlk:combat/sap_loop
execute if entity @s[tag=rlk_mb_body,tag=miniboss] if score #mbSap mb matches 1.. run scoreboard players operation #sapN tmp = #mbSap mb
execute if entity @s[tag=rlk_mb_body,tag=miniboss] if score #mbSap mb matches 1.. run function rlk:combat/sap_loop
execute unless score #gv tmp matches 1.. run return 0
execute store result storage rlk:ho mx double 0.01 run random value -14..14
execute store result storage rlk:ho mz double 0.01 run random value -14..14
function rlk:combat/gold_spawn with storage rlk:ho
scoreboard players operation @e[tag=rlk_goldnew] gval = #gv tmp
scoreboard players set @e[tag=rlk_goldnew] life 0
tag @e[tag=rlk_goldnew] remove rlk_goldnew
