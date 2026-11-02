# Test 22: heal the player 30 % of max HP (the existing player/heal: it clears the bond first).
execute as @a[tag=player,limit=1] run scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp /= #c100 kn
scoreboard players set #t kn 30
scoreboard players operation #heal tmp *= #t kn
execute as @a[tag=player,limit=1] run function rlk:player/heal
