# 잠식 +#g (@s = 몹). 최대 #rnErMax
scoreboard players operation @s rnEr += #g tmp
execute if score @s rnEr > #rnErMax tmp run scoreboard players operation @s rnEr = #rnErMax tmp
scoreboard players operation @s rnErT = #rnErHold tmp
scoreboard players set @s elAct 1
