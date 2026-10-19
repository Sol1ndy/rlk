# @s = body: the body push request (N12, cm.md 13.5; #mbPushOn is a per-tick request): only in the proxy state
# normal, the anchor moved <= 0.15 b/t and turned <= 6 deg/t since the last tick, no 42 mask round with safe
# markers, no pattern request #azNoPush (charge run, leap, whip pivot, emerge before out), not in a leap.
scoreboard players set #azMov mb 0
execute store result score #azX mb run data get entity @s Pos[0] 1000
execute store result score #azZ mb run data get entity @s Pos[2] 1000
execute store result score #azY mb run data get entity @s Rotation[0] 100
scoreboard players operation #azDX mb = #azX mb
scoreboard players operation #azDX mb -= #azLX mb
scoreboard players operation #azDZ mb = #azZ mb
scoreboard players operation #azDZ mb -= #azLZ mb
scoreboard players operation #azDY mb = #azY mb
scoreboard players operation #azDY mb -= #azLY mb
execute unless score #azDX mb matches -150..150 run scoreboard players set #azMov mb 1
execute unless score #azDZ mb matches -150..150 run scoreboard players set #azMov mb 1
execute unless score #azDY mb matches -600..600 run scoreboard players set #azMov mb 1
scoreboard players operation #azLX mb = #azX mb
scoreboard players operation #azLZ mb = #azZ mb
scoreboard players operation #azLY mb = #azY mb
execute unless score #azPx mb matches 0 run return 0
execute if score #azMov mb matches 1 run return 0
execute if score #azNoPush mb matches 1 run return 0
execute if score #azLeap mb matches 1 run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,limit=1] run return 0
scoreboard players set #mbPushOn mb 1
