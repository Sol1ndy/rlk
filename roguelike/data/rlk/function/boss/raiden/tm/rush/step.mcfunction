# @s = the boss, ticks 23-26: S + D * (rdTime - 22) / 4 (yaw kept).
scoreboard players operation #rdTmK rd = @s rdTime
scoreboard players remove #rdTmK rd 22
scoreboard players set #rdTm4 rd 4
scoreboard players operation #rdTmX rd = #rdTmDX rd
scoreboard players operation #rdTmX rd *= #rdTmK rd
scoreboard players operation #rdTmX rd /= #rdTm4 rd
scoreboard players operation #rdTmX rd += #rdTmSX rd
execute store result entity @e[tag=rlk_rd_tm_step,limit=1] Pos[0] double 0.001 run scoreboard players get #rdTmX rd
scoreboard players operation #rdTmZ rd = #rdTmDZ rd
scoreboard players operation #rdTmZ rd *= #rdTmK rd
scoreboard players operation #rdTmZ rd /= #rdTm4 rd
scoreboard players operation #rdTmZ rd += #rdTmSZ rd
execute store result entity @e[tag=rlk_rd_tm_step,limit=1] Pos[2] double 0.001 run scoreboard players get #rdTmZ rd
execute at @e[tag=rlk_rd_tm_step,limit=1] run tp @s ~ ~ ~
