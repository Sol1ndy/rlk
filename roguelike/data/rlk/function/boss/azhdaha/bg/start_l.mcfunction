# g.bg_start("L"): the calling pattern moves into bg slot L (clock #azBgLT 0 = this tick).
scoreboard players operation #azBgL mb = #azCast mb
execute unless score #azBgL mb matches 1.. run scoreboard players operation #azBgL mb = #azCast mb
scoreboard players set #azBgLT mb -1
