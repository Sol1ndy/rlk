# @s = the player: #bfDewNeed = 1 when one orb's effective heal (13 % of max HP rounded up, x the
# healing received %, rounded half up as mboss/player_heal does) fills the cure meter to its target, else 2.
scoreboard players operation #bfDewQ mb = @s maxHealth
scoreboard players operation #bfDewQ mb *= #bfDewPct mb
scoreboard players add #bfDewQ mb 99
scoreboard players operation #bfDewQ mb /= #c100 mb
scoreboard players operation #bfDewQ mb *= #mbHealPct mb
scoreboard players add #bfDewQ mb 50
scoreboard players operation #bfDewQ mb /= #c100 mb
scoreboard players operation #bfDewQ mb += #bfCure mb
scoreboard players set #bfDewNeed mb 2
execute if score #bfDewQ mb >= #bfCureT mb run scoreboard players set #bfDewNeed mb 1
