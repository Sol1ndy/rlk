execute unless score #rdCap rd matches 1 run return 0
function rlk:boss/raiden/caption/expire
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
scoreboard players set @a[tag=player,scores={vBig=1..}] vBig 0
