# 장미탄에 맞은 적 하나 (@s = 몹, at @s): 공격력의 #nvBase% × (100 + 맞은 발수² × 0.83)% × (100 + 15 × (소모 파편 - 3))%  바위 원소 · 원소전투 스킬 피해
execute store result storage rlk:nv c.coef int 1 run scoreboard players get #nvBase tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:nv c
scoreboard players operation #t1 tmp = @s nvHit
scoreboard players operation #t1 tmp *= @s nvHit
scoreboard players operation #t1 tmp *= #c83 tmp
scoreboard players operation #t1 tmp /= #100 tmp
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players operation #t1 tmp = #nvU tmp
scoreboard players remove #t1 tmp 3
execute if score #t1 tmp matches ..0 run scoreboard players set #t1 tmp 0
scoreboard players operation #t1 tmp *= #c15 tmp
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp
scoreboard players set #elem tmp 5
scoreboard players set #elU tmp 1000
scoreboard players operation #dmgBase tmp = #dmg tmp
function rlk:combat/apply
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1 ~ 0.3 0.4 0.3 0.1 8
scoreboard players set @s nvHit 0
