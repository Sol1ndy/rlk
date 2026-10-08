scoreboard players operation #t1 eng = @s energyRecharge
scoreboard players operation #t1 eng *= #emblemPct tmp
scoreboard players operation #t1 eng /= #100 tmp
execute if score #t1 eng > #emblemMax tmp run scoreboard players operation #t1 eng = #emblemMax tmp
scoreboard players add #t1 eng 100
scoreboard players operation #dmg tmp *= #t1 eng
scoreboard players operation #dmg tmp /= #100 tmp
