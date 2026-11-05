# The 5 % instant death (ULT5_LETHAL true; @s = the player; F:boss/raiden/hazard/fatal's model): skipped while the player
# revives; else all current HP as the hit (the number, Electro), curHealth 0, player/die. It bypasses mboss/hurt (dash
# i-frames and every shield are ignored); Ronova's one revive still applies; in a test the death ends in test/defeat.
execute if score @s rnDie matches 1.. run return 0
scoreboard players operation #hurtDmg tmp = @s curHealth
scoreboard players set #elem tmp 3
function rlk:player/hurt_do
scoreboard players set @s curHealth 0
function rlk:player/die
