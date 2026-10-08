scoreboard players operation #hl tmp = @s hurtLv
scoreboard players remove #hl tmp 1
scoreboard players operation #hl tmp *= #mobLvAtk tmp
scoreboard players add #hl tmp 100
scoreboard players operation #dmgIn tmp *= #hl tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
