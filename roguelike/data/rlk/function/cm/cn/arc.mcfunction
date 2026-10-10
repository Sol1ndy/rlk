execute store result score @s cmPx run data get entity @s Pos[0] 1000
execute store result score @s cmPy run data get entity @s Pos[1] 1000
execute store result score @s cmPz run data get entity @s Pos[2] 1000
execute store result score #tx tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #ty tmp run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #tz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
scoreboard players operation #tx tmp -= @s cmPx
scoreboard players operation #ty tmp -= @s cmPy
scoreboard players operation #tz tmp -= @s cmPz
# 수평 거리 ≈ 큰 쪽 + 작은 쪽 × 0.4
scoreboard players operation #ax tmp = #tx tmp
execute if score #ax tmp matches ..-1 run scoreboard players operation #ax tmp *= #m1 tmp
scoreboard players operation #az tmp = #tz tmp
execute if score #az tmp matches ..-1 run scoreboard players operation #az tmp *= #m1 tmp
scoreboard players operation #hm tmp = #ax tmp
scoreboard players operation #hm tmp > #az tmp
scoreboard players operation #hn tmp = #ax tmp
scoreboard players operation #hn tmp < #az tmp
scoreboard players operation #hn tmp *= #2 tmp
scoreboard players operation #hn tmp /= #5 tmp
scoreboard players operation #hm tmp += #hn tmp
# N = 18 + 거리(칸) × 1.2
scoreboard players operation #n tmp = #hm tmp
scoreboard players operation #n tmp *= #6 tmp
scoreboard players operation #n tmp /= #5000 tmp
scoreboard players add #n tmp 18
scoreboard players operation @s cmVx = #tx tmp
scoreboard players operation @s cmVx /= #n tmp
scoreboard players operation @s cmVz = #tz tmp
scoreboard players operation @s cmVz /= #n tmp
# vy = dy/N + g(N-1)/2
scoreboard players operation @s cmVy = #ty tmp
scoreboard players operation @s cmVy /= #n tmp
scoreboard players operation #t1 tmp = #n tmp
scoreboard players remove #t1 tmp 1
scoreboard players operation #t1 tmp *= #15 tmp
scoreboard players operation @s cmVy += #t1 tmp
scoreboard players operation @s cmT = #n tmp
scoreboard players add @s cmT 20
scoreboard players operation @s cmD = #cmD_cn tmp
scoreboard players operation @s cmLv = #clv tmp
scoreboard players set @s cmEl 0
# 떨어질 자리 표시
scoreboard players add #cmK tmp 1
scoreboard players operation @s cmN = #cmK tmp
scoreboard players operation #wdT tmp = #n tmp
scoreboard players operation #wdT tmp += #cmW_cnD tmp
# 궤적을 미리 따라가 봐서 장애물에 먼저 막히면 표시하지 않음
function rlk:cm/cn/sim
execute if score #blk tmp matches 0 at @e[tag=rlk_body,limit=1] run function rlk:cm/gnd {k:"cn"}
