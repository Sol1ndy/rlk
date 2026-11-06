# 때린 몹의 레벨 보정 (@s = 플레이어): x = hurtLv - 1, 원피해 × (100 + #mobLvAtk·x + #mobLvAtk2·x²/100)%
scoreboard players operation #hx tmp = @s hurtLv
scoreboard players remove #hx tmp 1
scoreboard players operation #hq tmp = #hx tmp
scoreboard players operation #hq tmp *= #hx tmp
scoreboard players operation #hq tmp *= #mobLvAtk2 tmp
scoreboard players operation #hq tmp /= #100 tmp
scoreboard players operation #hl tmp = #hx tmp
scoreboard players operation #hl tmp *= #mobLvAtk tmp
scoreboard players add #hl tmp 100
scoreboard players operation #hl tmp += #hq tmp
scoreboard players operation #dmgIn tmp *= #hl tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
