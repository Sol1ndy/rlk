execute unless score #mbLn mb matches 1 run return 0
scoreboard players set #mbLn mb 0
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
