# g.bg_start("T"): the calling pattern moves into bg slot T (clock #azBgTT 0 = this tick).
scoreboard players operation #azBgT mb = #azPat mb
execute unless score #azBgT mb matches 1.. run scoreboard players operation #azBgT mb = #azPat mb
scoreboard players set #azBgTT mb -1
