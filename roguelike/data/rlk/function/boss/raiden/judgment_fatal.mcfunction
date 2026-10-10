# This announced encounter mechanic requires the flower dome, not a timed dash.
# Setting custom HP to zero preserves the existing death / Ronova revival flow.
execute if score @s dead matches 1 run return 0
execute if score @s rnDie matches 1.. run return 0
scoreboard players operation #hurtDmg tmp = @s curHealth
scoreboard players set #elem tmp 3
function rlk:player/hurt_do
scoreboard players set @s curHealth 0
function rlk:player/die
