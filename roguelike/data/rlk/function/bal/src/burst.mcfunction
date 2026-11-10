scoreboard players operation #d bal = #now bal
scoreboard players operation #d bal -= @s balQ
execute if score #d bal < #burstGap bal run return 0
scoreboard players operation @s balQ = #now bal
scoreboard players operation #n bal += #burst bal
