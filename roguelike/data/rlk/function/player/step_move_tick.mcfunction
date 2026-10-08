# 살짝 전진 중 (@s = 플레이어, at 몸 rotated ~ 0). player/dash_move_tick 과 같은 이동, 대쉬 효과·아이템 발동은 없다
scoreboard players operation #subx tmp = @s dashDX
scoreboard players operation #subx tmp /= #st4 tmp
scoreboard players operation #subz tmp = @s dashDZ
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
scoreboard players remove @s stepT 1
