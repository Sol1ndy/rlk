# State set "inv" of cproto: membership, live / parked, the push capsules (tenths, anchor frame), the rig
# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).
data modify storage rlk:mboss px.set set value "inv"
scoreboard players set #pxS1 mb 0
scoreboard players set #pxS2 mb 0
function rlk:mboss/px/cproto/ev/1
function rlk:mboss/px/cproto/ev/2
data modify storage rlk:mboss push set value []
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] unless entity @s[tag=rlk_mb_inv] run function rlk:mboss/px/inv_on
