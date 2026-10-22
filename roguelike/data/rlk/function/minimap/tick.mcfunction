# From rlk:tick. Every 2 ticks: show/hide, and redraw when something changed.
scoreboard players add #mmT mm 1
execute if score #mmT mm matches 2.. run scoreboard players set #mmT mm 0
execute unless score #mmT mm matches 0 run return 0
scoreboard players set #mmShow mm 1
execute unless score #active room matches 1 run scoreboard players set #mmShow mm 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run scoreboard players set #mmShow mm 0
execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mmShow mm 0
execute if entity @a[tag=player,scores={vMap=1..}] run scoreboard players set #mmShow mm 0
# Boss fight: Narukami is there (any phase, arena or test), or the player is in a boss zone.
execute if entity @e[tag=rlk_raiden,limit=1] run scoreboard players set #mmShow mm 0
# Mid-boss fight: the player is in the separate circular arena, outside the grid.
execute if score #mbOn mb matches 1 run scoreboard players set #mmShow mm 0
execute if score #mmShow mm matches 0 run return run bossbar set rlk:minimap visible false
execute unless score #mmBuilt mm matches 1 run function rlk:minimap/build
function rlk:minimap/signature
scoreboard players set #pz mm 0
execute if score #pc mm matches 0.. run function rlk:minimap/player_zone
execute if score #pz mm matches 1.. as @e[tag=rlk_zone,scores={zkind=9}] if score @s zid = #pz mm run return run bossbar set rlk:minimap visible false
bossbar set rlk:minimap players @a[tag=player]
bossbar set rlk:minimap visible true
function rlk:minimap/facing
scoreboard players add #mmAge mm 1
execute if score #mmAge mm matches 20.. run scoreboard players set #mmSig mm -1
execute unless score #mmNew mm = #mmSig mm run return run function rlk:minimap/draw
execute unless score #mmDir mm = #mmDirS mm run function rlk:minimap/arrow
