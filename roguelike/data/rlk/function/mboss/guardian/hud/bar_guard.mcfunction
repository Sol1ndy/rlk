# @s = body: the leading element's record progress (count x 100 / needed) in its colour; gold time left
# before the first counted hit.
scoreboard players set #gdBest mb -1
scoreboard players set #gdBestE mb 0
scoreboard players operation #gdX mb = #gdN1 mb
scoreboard players operation #gdX mb *= #c100 mb
scoreboard players operation #gdX mb /= #gdQ1 mb
execute if score #gdN1 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players set #gdBestE mb 1
execute if score #gdN1 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players operation #gdBest mb = #gdX mb
scoreboard players operation #gdX mb = #gdN2 mb
scoreboard players operation #gdX mb *= #c100 mb
scoreboard players operation #gdX mb /= #gdQ2 mb
execute if score #gdN2 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players set #gdBestE mb 2
execute if score #gdN2 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players operation #gdBest mb = #gdX mb
scoreboard players operation #gdX mb = #gdN3 mb
scoreboard players operation #gdX mb *= #c100 mb
scoreboard players operation #gdX mb /= #gdQ3 mb
execute if score #gdN3 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players set #gdBestE mb 3
execute if score #gdN3 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players operation #gdBest mb = #gdX mb
scoreboard players operation #gdX mb = #gdN4 mb
scoreboard players operation #gdX mb *= #c100 mb
scoreboard players operation #gdX mb /= #gdQ4 mb
execute if score #gdN4 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players set #gdBestE mb 4
execute if score #gdN4 mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players operation #gdBest mb = #gdX mb
execute if score #gdBestE mb matches 0 run scoreboard players set #buSub bu 150
execute if score #gdBestE mb matches 0 run scoreboard players operation #buSub bu -= #gdT mb
execute if score #gdBestE mb matches 0 run scoreboard players set #buSubMax bu 100
execute if score #gdBestE mb matches 0 run scoreboard players set #buSubCol bu 8
execute if score #gdBestE mb matches 0 run return 0
scoreboard players operation #buSub bu = #gdBest mb
scoreboard players set #buSubMax bu 100
execute if score #gdBestE mb matches 1 run scoreboard players set #buSubCol bu 2
execute if score #gdBestE mb matches 2 run scoreboard players set #buSubCol bu 3
execute if score #gdBestE mb matches 3 run scoreboard players set #buSubCol bu 1
execute if score #gdBestE mb matches 4 run scoreboard players set #buSubCol bu 4
