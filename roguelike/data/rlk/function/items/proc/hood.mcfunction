scoreboard players operation #t1 itv = @s mhpC
scoreboard players operation #t1 itv *= #100 tmp
scoreboard players operation #t2 itv = @s mhpM
scoreboard players operation #t2 itv *= #hoodHp tmp
execute if score #t1 itv <= #t2 itv run scoreboard players operation #eb eng += #hoodDmg tmp
