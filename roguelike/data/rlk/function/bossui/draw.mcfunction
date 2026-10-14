# As the boss, with #buHp #buMax #buSub #buSubMax #buSubCol set: line -> storage rlk:bu line.
execute if score #buMax bu matches ..0 run scoreboard players set #buMax bu 1
execute if score #buHp bu matches ..-1 run scoreboard players set #buHp bu 0
function rlk:bossui/trail
data modify storage rlk:bu line set value []
scoreboard players operation #fill bu = #buHp bu
scoreboard players operation #fill bu *= #bar bu
scoreboard players operation #fill bu /= #buMax bu
execute if score #buHp bu matches 1.. if score #fill bu matches ..0 run scoreboard players set #fill bu 1
scoreboard players operation #tr bu = @s buTrail
scoreboard players operation #tr bu *= #bar bu
scoreboard players operation #tr bu /= #buMax bu
execute if score #tr bu < #fill bu run scoreboard players operation #tr bu = #fill bu
scoreboard players operation #white bu = #tr bu
scoreboard players operation #white bu -= #fill bu
scoreboard players operation #empty bu = #bar bu
scoreboard players operation #empty bu -= #tr bu
execute if score #empty bu matches ..-1 run scoreboard players set #empty bu 0
scoreboard players operation #len bu = #fill bu
function rlk:bossui/run_hp {col:"#E0484B"}
scoreboard players operation #len bu = #white bu
function rlk:bossui/run_hp {col:"#FFFFFF"}
scoreboard players operation #len bu = #empty bu
function rlk:bossui/run_hp {col:"#2A2A2E"}
# Numbers "hp/max" centred on the bar (default font, 6 px per character).
scoreboard players set #n bu 1
scoreboard players set #nh bu 1
scoreboard players set #nm bu 1
execute if score #buHp bu matches 1.. run scoreboard players set #nh bu 1
execute if score #buMax bu matches 1.. run scoreboard players set #nm bu 1
execute if score #buHp bu matches 10.. run scoreboard players set #nh bu 2
execute if score #buMax bu matches 10.. run scoreboard players set #nm bu 2
execute if score #buHp bu matches 100.. run scoreboard players set #nh bu 3
execute if score #buMax bu matches 100.. run scoreboard players set #nm bu 3
execute if score #buHp bu matches 1000.. run scoreboard players set #nh bu 4
execute if score #buMax bu matches 1000.. run scoreboard players set #nm bu 4
execute if score #buHp bu matches 10000.. run scoreboard players set #nh bu 5
execute if score #buMax bu matches 10000.. run scoreboard players set #nm bu 5
execute if score #buHp bu matches 100000.. run scoreboard players set #nh bu 6
execute if score #buMax bu matches 100000.. run scoreboard players set #nm bu 6
execute if score #buHp bu matches 1000000.. run scoreboard players set #nh bu 7
execute if score #buMax bu matches 1000000.. run scoreboard players set #nm bu 7
scoreboard players operation #n bu += #nh bu
scoreboard players operation #n bu += #nm bu
scoreboard players operation #w bu = #n bu
scoreboard players operation #w bu *= #digit bu
scoreboard players operation #half bu = #w bu
scoreboard players operation #half bu /= #2 bu
# back from the bar end to the text start: BAR/2 + w/2
scoreboard players set #len bu 100
scoreboard players operation #len bu += #half bu
function rlk:bossui/space_neg
# The nbt component joins the list as children of its first entry (a bar piece in font
# rlk:bossbar), so the numbers must name the default font or they inherit the bar font.
data modify storage rlk:bu line append value {score:{name:"#buHp",objective:"bu"},color:"white",font:"minecraft:default"}
data modify storage rlk:bu line append value {text:"/",color:"#D0D0D0",font:"minecraft:default"}
data modify storage rlk:bu line append value {score:{name:"#buMax",objective:"bu"},color:"#D0D0D0",font:"minecraft:default"}
# forward to the bar end again: BAR/2 - w/2
scoreboard players set #len bu 100
scoreboard players operation #len bu -= #half bu
execute if score #len bu matches 1.. run function rlk:bossui/space_pos
# Under bar (shield in its element colour, or a gauge).
execute if score #buSubCol bu matches 1.. if score #buSubMax bu matches 1.. run function rlk:bossui/sub
