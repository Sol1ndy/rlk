# @s = 플레이어 (player/dash_dir: 더블 닷지의 옆돌기, 방향키 없음). 원작의 두 번째 동작은 옆으로 돌며 뒤로 물러나 내린다: 기준 =
# 앞쪽(시선의 앞 반쪽) 8칸 안에서 가장 가까운 적(rlk_mob), 없으면 몸이 보는 쪽. 그 기준에서 오른쪽 뒤 135도 / 왼쪽 뒤 135도로 — 옆돌기마다
# 번갈아(#dgSide cb: 홀수 = 오른쪽, 짝수 = 왼쪽, 첫 번째는 오른쪽). 적 쪽으로는 가지 않는다(앞으로 0.58칸 들어가던 것, 통합 11-12).
# 결과는 #ux · #uz(단위 × 100, player/dash_norm)
scoreboard players add #dgSide cb 1
scoreboard players operation #t1 tmp = #dgSide cb
scoreboard players operation #t1 tmp %= #2 tmp
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^ ^8 run tag @e[tag=rlk_mob,distance=..8] add rlk_dgfr
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_dgfr,distance=..8,sort=nearest,limit=1] run tag @s add rlk_dgref
tag @e[tag=rlk_dgfr] remove rlk_dgfr
execute store result score #cx tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #cz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
execute if entity @e[tag=rlk_dgref,limit=1] if score #t1 tmp matches 1 at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_dgref,limit=1] feet rotated ~135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if entity @e[tag=rlk_dgref,limit=1] if score #t1 tmp matches 0 at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_dgref,limit=1] feet rotated ~-135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute unless entity @e[tag=rlk_dgref,limit=1] if score #t1 tmp matches 1 at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute unless entity @e[tag=rlk_dgref,limit=1] if score #t1 tmp matches 0 at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~-135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
tag @e[tag=rlk_dgref] remove rlk_dgref
execute store result score #vx tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[0] 100
execute store result score #vz tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
scoreboard players operation #vx tmp -= #cx tmp
scoreboard players operation #vz tmp -= #cz tmp
function rlk:player/dash_norm
