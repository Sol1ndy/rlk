# 공격력% += 골드 ÷ #treasurePer (최대 #treasureMax)
scoreboard players operation #t1 eng = @s gold
scoreboard players operation #t1 eng /= #treasurePer tmp
execute if score #t1 eng > #treasureMax tmp run scoreboard players operation #t1 eng = #treasureMax tmp
execute if score #t1 eng matches 1.. run scoreboard players operation @s atkPct += #t1 eng
