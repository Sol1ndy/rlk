# Jumpable wave: feet more than0.75 above the ground passed the early height gate.
execute if score @s rdHHit matches 1 run return 0
scoreboard players operation #rdElapsed rd = @s rdHAge
scoreboard players operation #rdElapsed rd -= @s rdWind
execute unless score #rdElapsed rd matches 0..31 run return 0
scoreboard players operation #rdRadius rd = #rdElapsed rd
scoreboard players set #rdSpan rd 16000
scoreboard players operation #rdRadius rd *= #rdSpan rd
scoreboard players set #rdSteps rd 31
scoreboard players operation #rdRadius rd /= #rdSteps rd
scoreboard players add #rdRadius rd 2000
scoreboard players operation #rdInner rd = #rdRadius rd
scoreboard players remove #rdInner rd 700
scoreboard players operation #rdInner rd *= #rdInner rd
scoreboard players operation #rdOuter rd = #rdRadius rd
scoreboard players add #rdOuter rd 700
scoreboard players operation #rdOuter rd *= #rdOuter rd
execute if score #rdR2 rd >= #rdInner rd if score #rdR2 rd <= #rdOuter rd run scoreboard players set #rdHit rd 1
