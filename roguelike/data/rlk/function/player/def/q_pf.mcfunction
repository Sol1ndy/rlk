# @s = 플레이어, #qn cb = 볼 틱. 그 틱이 닷지의 퍼펙트 창(dgAt + 0..#dgPW-1) 또는 F 의 3단계 창(parAt + 0..#parW3-1) 안이면 1
scoreboard players operation #q cb = #qn cb
scoreboard players operation #q cb -= @s dgAt
execute if score #q cb matches 0.. if score #q cb < #dgPW tmp run return 1
scoreboard players operation #q cb = #qn cb
scoreboard players operation #q cb -= @s parAt
execute if score #q cb matches 0.. if score #q cb < #parW3 tmp run return 1
return fail
