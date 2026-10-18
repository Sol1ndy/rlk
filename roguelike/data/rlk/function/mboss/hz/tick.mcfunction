# @s = hazard marker, at/rotated as @s (world tick; frozen while the fight is paused).
scoreboard players set #mbHzOn mb 1
scoreboard players add @s mbHzT 1
execute if score @s mbHzT >= @s mbHzL run return run function rlk:mboss/hz/expire
scoreboard players operation #t mb = @s mbHzT
scoreboard players operation #t mb %= #c4 mb
execute if score @s mbHzT < @s mbHzW if score #t mb matches 0 unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/draw
execute if score @s mbHzT = @s mbHzW run function rlk:mboss/hz/strike
scoreboard players operation #hzEnd mb = @s mbHzW
scoreboard players operation #hzEnd mb += @s mbHzA
# dmg 0 = telegraph only (outline, strike flash and the module visuals; never a hit)
execute if score @s mbHzHit matches 0 if score @s mbHzD matches 1.. if score @s mbHzT >= @s mbHzW if score @s mbHzT < #hzEnd mb run function rlk:mboss/hz/hit
