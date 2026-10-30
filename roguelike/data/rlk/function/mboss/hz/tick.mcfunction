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
# #hzRearm: a hit (or a hit of its volley group) disarmed it until the re-arm clock reaches mbHzRT
execute if score @s mbHzHit matches 1 if score @s mbHzRA matches 1.. if score #mbHzClk mb >= @s mbHzRT run scoreboard players set @s mbHzHit 0
# dmg 0 = telegraph only (outline, strike flash and the module visuals; never a hit)
execute if score @s mbHzHit matches 0 if score @s mbHzD matches 1.. if score @s mbHzT >= @s mbHzW if score @s mbHzT < #hzEnd mb run function rlk:mboss/hz/hit
