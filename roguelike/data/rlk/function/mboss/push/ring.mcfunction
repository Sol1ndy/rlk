# {r,to,kb} (as anything, at the centre; cm.md 13.5 / N18): a push-only ring. A player whose body is within r (tenths,
# horizontal) is moved radially outward to the distance to (tenths, to >= r) on its bearing over kb ticks (1..10; the
# collision-checked pull glide, no facing turn); a player at the centre goes toward the arena start. Skipped when the
# landing point is inside a live disc / ring / line hazard. No damage, no hit event, not dodgeable. r <= 320 and to <= 600
# (larger values are clamped: the squared distances stay inside int32, every offset beyond 32 b is outside the ring).
$scoreboard players set #prR mb $(r)
$scoreboard players set #prTo mb $(to)
$scoreboard players set #prKb mb $(kb)
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute if score #prR mb matches 321.. run scoreboard players set #prR mb 320
execute if score #prTo mb matches 601.. run scoreboard players set #prTo mb 600
execute if score #prTo mb < #prR mb run scoreboard players operation #prTo mb = #prR mb
execute if score #prKb mb matches ..0 run scoreboard players set #prKb mb 1
execute if score #prKb mb matches 11.. run scoreboard players set #prKb mb 10
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_prc"]}
execute store result score #qcx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_prc,limit=1] Pos[0] 1000
execute store result score #qcz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_prc,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_mb_prc]
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #pbx mb = #mbPX mb
scoreboard players operation #pbz mb = #mbPZ mb
scoreboard players operation #qx mb = #pbx mb
scoreboard players operation #qx mb -= #qcx mb
scoreboard players operation #qz mb = #pbz mb
scoreboard players operation #qz mb -= #qcz mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #n mb = #qx mb
scoreboard players operation #n mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #n mb += #t mb
scoreboard players operation #t mb = #prR mb
scoreboard players operation #t mb *= #c100 mb
scoreboard players operation #t mb *= #t mb
execute if score #n mb > #t mb run return 0
scoreboard players set #pd mb 0
execute if score #n mb matches 1.. run function rlk:mboss/push/sqrt
execute if score #pd mb matches ..49 run function rlk:mboss/push/ring_start
execute if score #pd mb matches ..49 run return 0
function rlk:mboss/push/ring_land
