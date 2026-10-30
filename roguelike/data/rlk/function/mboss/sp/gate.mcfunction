# From room/rift/enter (@s = an open rift's anchor, at it: the player walked in or clicked it). Mirrors mboss/gate +
# cb/gate: peaceful refuses (sp/no_peace), a running fight or a locked room refuses silently, then the special of the
# anchor's zone (zone data.rift.id; literal lines per special) enters through sp/g/<id>. Returns 1 when the fight
# starts, 0 when refused (room/rift/enter then holds the rift for 40 t).
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run function rlk:mboss/sp/no_peace
execute if entity @e[tag=rlk_mb_body,limit=1] run return 0
execute if score #mbLive mb matches 1 run return 0
execute if score #combat room matches 1.. run return 0
tag @e[tag=rlk_spz] remove rlk_spz
scoreboard players operation #spZ mb = @s zid
execute as @e[type=minecraft:marker,tag=rlk_zone,tag=rlk_riftz] if score @s zid = #spZ mb run tag @s add rlk_spz
execute unless entity @e[tag=rlk_spz,limit=1] run return 0
data modify storage rlk:mboss spg set value ""
data modify storage rlk:mboss spg set from entity @e[tag=rlk_spz,limit=1] data.rift.id
execute if data storage rlk:mboss {spg:"tachy"} run return run function rlk:mboss/sp/g/tachy
execute if data storage rlk:mboss {spg:"spproto"} run return run function rlk:mboss/sp/g/spproto
tag @e[tag=rlk_spz] remove rlk_spz
return 0
