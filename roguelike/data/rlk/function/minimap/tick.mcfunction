# From rlk:tick. Every 5 ticks: show/hide, and redraw when something changed.
scoreboard players add #mmT mm 1
execute if score #mmT mm matches 5.. run scoreboard players set #mmT mm 0
execute unless score #mmT mm matches 0 run return 0
scoreboard players set #mmShow mm 1
execute unless score #active room matches 1 run scoreboard players set #mmShow mm 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run scoreboard players set #mmShow mm 0
execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mmShow mm 0
execute if entity @a[tag=player,scores={vMap=1..}] run scoreboard players set #mmShow mm 0
execute if entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run scoreboard players set #mmShow mm 0
execute if score #mmShow mm matches 0 run return run bossbar set rlk:minimap visible false
bossbar set rlk:minimap players @a[tag=player]
bossbar set rlk:minimap visible true
function rlk:minimap/signature
scoreboard players add #mmAge mm 1
execute if score #mmAge mm matches 8.. run scoreboard players set #mmSig mm -1
execute unless score #mmNew mm = #mmSig mm run function rlk:minimap/draw
