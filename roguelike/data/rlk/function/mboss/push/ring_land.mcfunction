# The landing point = centre + (#qx, #qz) / #pd x to (mb); then the glide unless it lands inside a live hazard.
scoreboard players operation #t mb = #prTo mb
scoreboard players operation #t mb *= #c100 mb
scoreboard players operation #peX mb = #qx mb
scoreboard players operation #peX mb *= #t mb
scoreboard players operation #peX mb /= #pd mb
scoreboard players operation #peX mb += #qcx mb
scoreboard players operation #peZ mb = #qz mb
scoreboard players operation #peZ mb *= #t mb
scoreboard players operation #peZ mb /= #pd mb
scoreboard players operation #peZ mb += #qcz mb
function rlk:mboss/push/end_ok
execute if score #pOK mb matches 0 run return 0
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_prl"]}
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] Pos[0] double 0.001 run scoreboard players get #peX mb
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] Pos[2] double 0.001 run scoreboard players get #peZ mb
execute store result storage rlk:mboss a.t int 1 run scoreboard players get #prKb mb
scoreboard players set #pullFace mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_prl,limit=1] run function rlk:mboss/push/ring_go with storage rlk:mboss a
kill @e[type=minecraft:marker,tag=rlk_mb_prl]
