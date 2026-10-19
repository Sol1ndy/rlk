# @s = the branded player: the cure meter (cumulative healing while branded) reaching 6 % max HP cleanses.
scoreboard players operation #azHeal mb += #mbHealAmt mb
scoreboard players set #mbHealAmt mb 0
scoreboard players operation #azX mb = @s maxHealth
scoreboard players set #azY mb 6
scoreboard players operation #azX mb *= #azY mb
scoreboard players operation #azY mb = #azHeal mb
scoreboard players operation #azY mb *= #c100 mb
execute if score #azY mb >= #azX mb run function rlk:mboss/azhdaha/brand/cleanse
