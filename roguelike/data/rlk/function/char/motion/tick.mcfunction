# Combat active state remains separate from persistent locomotion visibility.
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 run return run function rlk:char/motion/cleanup
execute if score @s dead matches 1 run return run function rlk:char/motion/cleanup
execute if score @s vMap matches 1 run return run function rlk:char/motion/cleanup
execute if score @s pkMode matches 1.. run return run function rlk:char/motion/cleanup
execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:char/motion/cleanup
execute if score @s pmActive matches 1 unless score @s pmChar = #charN tmp run function rlk:char/motion/stop
execute if score @s pmVisible matches 1 unless score @s pmRigChar = #charN tmp run function rlk:char/motion/stop
execute unless entity @e[tag=rlk_av,limit=1] run kill @e[tag=rlk_pm]
execute unless entity @e[tag=rlk_av,limit=1] run scoreboard players set @s pmVisible 0
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/observe
execute if score @s pmActive matches 1 run return run function rlk:char/motion/combat_tick
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/tick
