# State set "p1" of apep: membership, live / parked, the push capsules (tenths, anchor frame), the rig
# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).
data modify storage rlk:mboss px.set set value "p1"
scoreboard players set #pxS1 mb 1
scoreboard players set #pxS2 mb 1
scoreboard players set #pxS3 mb 1
scoreboard players set #pxS4 mb 1
scoreboard players set #pxS5 mb 1
scoreboard players set #pxS6 mb 1
scoreboard players set #pxS7 mb 1
scoreboard players set #pxS8 mb 1
scoreboard players set #pxS9 mb 1
scoreboard players set #pxS10 mb 1
scoreboard players set #pxS11 mb 1
function rlk:mboss/px/apep/ev/1
function rlk:mboss/px/apep/ev/2
function rlk:mboss/px/apep/ev/3
function rlk:mboss/px/apep/ev/4
function rlk:mboss/px/apep/ev/5
function rlk:mboss/px/apep/ev/6
function rlk:mboss/px/apep/ev/7
function rlk:mboss/px/apep/ev/8
function rlk:mboss/px/apep/ev/9
function rlk:mboss/px/apep/ev/10
function rlk:mboss/px/apep/ev/11
data modify storage rlk:mboss push set value [{f0:0,f1:20,hw:10,px:"",top:0},{f0:-22,f1:2,hw:12,px:"",top:0}]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/apep/rig_stub/state/normal
execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1] run function rlk:mboss/px/inv_off
