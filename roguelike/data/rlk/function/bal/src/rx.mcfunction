# strong reactions (#rx: 1 vaporize 2 melt 3 overload 4 superconduct 6 frozen 7 shatter 17 void burn 19 void judgement)
scoreboard players set #r bal 0
execute if score #rx tmp matches 1 run scoreboard players set #r bal 1
execute if score #rx tmp matches 2 run scoreboard players set #r bal 1
execute if score #rx tmp matches 3 run scoreboard players set #r bal 1
execute if score #rx tmp matches 4 run scoreboard players set #r bal 1
execute if score #rx tmp matches 6 run scoreboard players set #r bal 1
execute if score #rx tmp matches 7 run scoreboard players set #r bal 2
execute if score #rx tmp matches 17 run scoreboard players set #r bal 1
execute if score #rx tmp matches 19 run scoreboard players set #r bal 1
execute if score #r bal matches 0 run return 0
scoreboard players operation #d bal = #now bal
scoreboard players operation #d bal -= @s balX
execute if score #d bal < #rxGap bal run return 0
scoreboard players operation @s balX = #now bal
scoreboard players operation #n bal += #r bal
