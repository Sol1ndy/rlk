# sg/incoming during the guard (B-03..B-07): basic attacks (#icd 1, not a skill, not a reaction) are parried
# at x0.1 and fill the meter by 1; everything else passes at x0.5 and fills it by 2; 14 breaks it.
scoreboard players set #rdSgBasic rd 0
execute if score #icd tmp matches 1 unless score #skillDmg tmp matches 1 unless score #tfm tmp matches 1 run scoreboard players set #rdSgBasic rd 1
execute if score #rdSgBasic rd matches 1 run function rlk:boss/raiden/sg/guard_parry
execute if score #rdSgBasic rd matches 0 run scoreboard players operation #dmg tmp /= #rd2 rd
execute if score #rdSgBasic rd matches 0 run scoreboard players add @s rdSgGm 2
execute if score @s rdSgGm matches 14.. run function rlk:boss/raiden/sg/guard_break
