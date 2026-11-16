# State set "normal" of cproto: membership, live / parked, the push capsules (tenths, anchor frame), the rig
# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).
data modify storage rlk:mboss px.set set value "normal"
scoreboard players set #pxS1 mb 1
scoreboard players set #pxS2 mb 1
function rlk:mboss/px/cproto/ev/1
function rlk:mboss/px/cproto/ev/2
data modify storage rlk:mboss push set value [{f0:-12,f1:12,hw:12,px:"",top:0},{f0:-32,f1:-16,hw:6,px:"tail",top:15}]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1] run function rlk:mboss/px/inv_off
