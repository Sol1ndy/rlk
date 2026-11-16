# Combat active state remains separate from persistent locomotion visibility.
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 unless score #charN tmp matches 6 run return run function rlk:char/motion/cleanup
execute if score @s dead matches 1 run return run function rlk:char/motion/cleanup
execute if score @s vMap matches 1 run return run function rlk:char/motion/cleanup
execute if score @s pkMode matches 1.. run return run function rlk:char/motion/cleanup
execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:char/motion/cleanup
execute if score @s pmActive matches 1 unless score @s pmChar = #charN tmp run function rlk:char/motion/stop
execute if score @s pmVisible matches 1 unless score @s pmRigChar = #charN tmp run function rlk:char/motion/stop
execute unless entity @e[tag=rlk_av,limit=1] run kill @e[tag=rlk_pm]
execute unless entity @e[tag=rlk_av,limit=1] run scoreboard players set @s pmVisible 0
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/observe
# Weapon state first (it may start the put-away clip or blend locomotion into the sheathed set).
function rlk:char/motion/sheath/tick
# No locomotion on the tick a clip finished (finish already posed the blend).
execute store result score #pmWasActive tmp if score @s pmActive matches 1
execute if score #pmWasActive tmp matches 1 run function rlk:char/motion/combat_tick
execute if score #pmWasActive tmp matches 0 if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/tick
execute if score @s pmShFx matches 1.. run function rlk:char/motion/sheath/fx_tick
# Attach changes snap even when several authored ticks (or a start and its first advance) ran this tick.
execute if score #pmSnapW tmp matches 1 run function rlk:char/motion/sheath/snap_end
