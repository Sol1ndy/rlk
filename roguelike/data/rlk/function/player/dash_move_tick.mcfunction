# @s = 플레이어, at @s rotated ~ 0. 닷지 이동 한 틱: 이번 틱의 속도 #dgSp(player/dodge/speed, 칸 × 1000)를 서브스텝 4개로 나눠 옮긴다
# (서브스텝 하나 0.125칸 이하). 검사는 몸 앞면(중심+0.3칸)
function rlk:player/dodge/speed
scoreboard players operation #subx tmp = @s dashDX
scoreboard players operation #subx tmp *= #dgSp tmp
scoreboard players operation #subx tmp /= #1000 tmp
scoreboard players operation #subx tmp /= #st4 tmp
scoreboard players operation #subz tmp = @s dashDZ
scoreboard players operation #subz tmp *= #dgSp tmp
scoreboard players operation #subz tmp /= #1000 tmp
scoreboard players operation #subz tmp /= #st4 tmp
execute store result storage rlk:dm dx double 0.001 run scoreboard players get #subx tmp
execute store result storage rlk:dm dz double 0.001 run scoreboard players get #subz tmp
scoreboard players operation #chkx tmp = @s dashUX
scoreboard players operation #chkx tmp *= #st3 tmp
scoreboard players operation #chkx tmp += #subx tmp
scoreboard players operation #chkz tmp = @s dashUZ
scoreboard players operation #chkz tmp *= #st3 tmp
scoreboard players operation #chkz tmp += #subz tmp
execute store result storage rlk:dm cx double 0.001 run scoreboard players get #chkx tmp
execute store result storage rlk:dm cz double 0.001 run scoreboard players get #chkz tmp
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/dash_sub with storage rlk:dm
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/dash_sub with storage rlk:dm
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/dash_sub with storage rlk:dm
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/dash_sub with storage rlk:dm
scoreboard players remove @s dashMoveT 1
# 아이템 닷지 이동 중 트리거
function rlk:items/hook/on_dash_move
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cloud ~ ~0.1 ~ 0.08 0.02 0.08 0.005 1
