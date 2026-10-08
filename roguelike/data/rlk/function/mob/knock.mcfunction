# 넉백 (@s = 몹, at @s): 몸(플레이어·아바타)에서 멀어지는 수평 방향으로 #kbBasic(칸/틱 × 1000)만큼 밀고 살짝 띄운다
# 방향 = 표식을 "몸의 반대쪽 1칸"에 두고 (표식 위치 - 몹 위치) 로 구한 단위 벡터
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_kbm"]}
execute store result score #kx tmp run data get entity @e[tag=rlk_kbm,limit=1] Pos[0] 1000
execute store result score #kz tmp run data get entity @e[tag=rlk_kbm,limit=1] Pos[2] 1000
kill @e[tag=rlk_kbm]
execute store result score #t1 tmp run data get entity @s Pos[0] 1000
scoreboard players operation #kx tmp -= #t1 tmp
execute store result score #t1 tmp run data get entity @s Pos[2] 1000
scoreboard players operation #kz tmp -= #t1 tmp
scoreboard players operation #kx tmp *= #kbBasic tmp
scoreboard players operation #kx tmp /= #1000 tmp
scoreboard players operation #kz tmp *= #kbBasic tmp
scoreboard players operation #kz tmp /= #1000 tmp
execute store result entity @s Motion[0] double 0.001 run scoreboard players get #kx tmp
execute store result entity @s Motion[2] double 0.001 run scoreboard players get #kz tmp
execute if data entity @s {OnGround:1b} run data modify entity @s Motion[1] set value 0.12d
