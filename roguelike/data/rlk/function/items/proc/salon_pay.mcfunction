scoreboard players operation #t1 itv = @s curHealth
scoreboard players operation #t1 itv *= #st2 tmp
execute unless score #t1 itv > @s maxHealth run return 0
scoreboard players operation #t1 itv = @s maxHealth
scoreboard players operation #t1 itv *= #salonCost tmp
scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation @s curHealth -= #t1 itv
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
scoreboard players operation #t1 itv = #salonDmg tmp
scoreboard players add #t1 itv 100
scoreboard players operation #dmg tmp *= #t1 itv
scoreboard players operation #dmg tmp /= #100 tmp
