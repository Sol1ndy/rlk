# Line: -back <= fwd <= len and |side| <= half width (both with the body pad).
execute if score #fwd mb < @s mbHzLo run return 0
execute if score #fwd mb > @s mbHzHi run return 0
scoreboard players operation #side mb = #dx mb
scoreboard players operation #side mb *= @s mbHzFZ
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= @s mbHzFX
scoreboard players operation #side mb -= #t mb
scoreboard players operation #side mb /= #c1000 mb
execute if score #side mb matches ..-1 run scoreboard players operation #side mb *= #cm1 mb
execute if score #side mb <= @s mbHzHW run function rlk:mboss/hz/hurt
