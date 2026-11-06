# Thin bar under the HP bar: #buSub / #buSubMax in colour #buSubCol.
scoreboard players set #len bu 200
function rlk:bossui/space_neg
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
execute if score #buSub bu > #buSubMax bu run scoreboard players operation #buSub bu = #buSubMax bu
scoreboard players operation #sf bu = #buSub bu
scoreboard players operation #sf bu *= #bar bu
scoreboard players operation #sf bu /= #buSubMax bu
execute if score #buSub bu matches 1.. if score #sf bu matches ..0 run scoreboard players set #sf bu 1
scoreboard players operation #se bu = #bar bu
scoreboard players operation #se bu -= #sf bu
scoreboard players operation #len bu = #sf bu
execute if score #buSubCol bu matches 1 run function rlk:bossui/run_sub {col:"#C58BFF"}
execute if score #buSubCol bu matches 2 run function rlk:bossui/run_sub {col:"#FF8A3D"}
execute if score #buSubCol bu matches 3 run function rlk:bossui/run_sub {col:"#4FB8FF"}
execute if score #buSubCol bu matches 4 run function rlk:bossui/run_sub {col:"#9FE8F5"}
execute if score #buSubCol bu matches 5 run function rlk:bossui/run_sub {col:"#F2C14E"}
execute if score #buSubCol bu matches 6 run function rlk:bossui/run_sub {col:"#6FE3C1"}
execute if score #buSubCol bu matches 7 run function rlk:bossui/run_sub {col:"#A5D94A"}
execute if score #buSubCol bu matches 8 run function rlk:bossui/run_sub {col:"#E8C35A"}
execute if score #buSubCol bu matches 9 run function rlk:bossui/run_sub {col:"#7BD88F"}
scoreboard players operation #len bu = #se bu
function rlk:bossui/run_sub {col:"#1E1E22"}
