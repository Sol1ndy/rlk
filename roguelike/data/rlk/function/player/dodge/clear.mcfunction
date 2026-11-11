# @s = 플레이어 (player/dash_move_tick, 더블 닷지의 옆돌기). 적의 몸 속에서 끝나지 않는다: 이번 틱의 이동이 끝나는 자리 + 몸 반폭 0.3칸이
# 적(rlk_mob)의 0.7칸 안이면 이번 틱은 움직이지 않고 동작을 끝낸다(그 앞에서 멈춤)
scoreboard players operation #pcx tmp = @s dashUX
scoreboard players operation #pcx tmp *= #dgSp tmp
scoreboard players operation #pcx tmp /= #100 tmp
scoreboard players operation #t1 tmp = @s dashUX
scoreboard players operation #t1 tmp *= #3 tmp
scoreboard players operation #pcx tmp += #t1 tmp
scoreboard players operation #pcz tmp = @s dashUZ
scoreboard players operation #pcz tmp *= #dgSp tmp
scoreboard players operation #pcz tmp /= #100 tmp
scoreboard players operation #t1 tmp = @s dashUZ
scoreboard players operation #t1 tmp *= #3 tmp
scoreboard players operation #pcz tmp += #t1 tmp
execute store result storage rlk:dm px double 0.001 run scoreboard players get #pcx tmp
execute store result storage rlk:dm pz double 0.001 run scoreboard players get #pcz tmp
function rlk:player/dodge/clear2 with storage rlk:dm
