# @s = the player: the cure target #bfCureT = 15 % of max HP (rounded down, at least 1) and the readout for the
# kit (#bkCureP = the meter in % of max HP, rounded down, #bkCureT = the target %): the 달빛 고치 entry of the boss-bar
# sub-line ("회복 9/15%") and hud/ab_cure show them as score components.
scoreboard players operation #bfCureT mb = @s maxHealth
scoreboard players operation #bfCureT mb *= #bfCurePct mb
scoreboard players operation #bfCureT mb /= #c100 mb
execute if score #bfCureT mb matches ..0 run scoreboard players set #bfCureT mb 1
scoreboard players operation #bkCureP mb = #bfCure mb
scoreboard players operation #bkCureP mb *= #c100 mb
execute if score @s maxHealth matches 1.. run scoreboard players operation #bkCureP mb /= @s maxHealth
execute if score #bkCureP mb > #bfCurePct mb run scoreboard players operation #bkCureP mb = #bfCurePct mb
scoreboard players operation #bkCureT mb = #bfCurePct mb
