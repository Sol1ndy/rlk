scoreboard players operation #t1 itv = @s it_prayer_beads
scoreboard players operation #t1 itv *= #beadsHeal tmp
scoreboard players add #t1 itv 100
scoreboard players operation #heal tmp *= #t1 itv
scoreboard players operation #heal tmp /= #100 tmp
