scoreboard players operation #dashRegenT tmp *= #100 tmp
scoreboard players operation #t1 eng = #dashEngSpd tmp
scoreboard players add #t1 eng 100
scoreboard players operation #dashRegenT tmp /= #t1 eng
execute if score #dashRegenT tmp matches ..0 run scoreboard players set #dashRegenT tmp 1
