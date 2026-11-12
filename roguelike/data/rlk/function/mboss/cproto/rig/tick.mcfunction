# @s = body: one rig tick (the pose of mbT is shown this tick); a clip that ends loops, goes on or holds.
execute unless score @s mbT matches 0.. run return run scoreboard players set @s mbT 0
scoreboard players add @s mbT 1
execute if score @s mbS matches 1 if score @s mbT matches 40.. run scoreboard players set @s mbT 0
execute if score @s mbS matches 2 if score @s mbT matches 24.. run function rlk:mboss/cproto/rig/play {c:1}
execute if score @s mbS matches 3 if score @s mbT matches 20.. run scoreboard players set @s mbT 19
execute if score @s mbS matches 4 if score @s mbT matches 20.. run function rlk:mboss/cproto/rig/play {c:1}
function rlk:mboss/cproto/rig/follow
