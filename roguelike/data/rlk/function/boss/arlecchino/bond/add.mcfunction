# @s = the player, #bolPct tmp = % of max HP: the existing bond add (capped at #bolMax), the amount she added in
# #given (she takes back at most that at the end), her bond flag.
execute unless score @s bol matches 0.. run scoreboard players set @s bol 0
scoreboard players operation #t kn = @s bol
function rlk:player/bol/add_pct
scoreboard players operation #t2 kn = @s bol
scoreboard players operation #t2 kn -= #t kn
execute if score #t2 kn matches 1.. run scoreboard players operation #given kn += #t2 kn
scoreboard players set #bonded kn 1
