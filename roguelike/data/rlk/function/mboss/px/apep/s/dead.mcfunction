# State set "dead" of apep: membership, live / parked, the push capsules (tenths, anchor frame), the rig
# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).
data modify storage rlk:mboss px.set set value "dead"
scoreboard players set #pxS1 mb 0
scoreboard players set #pxS2 mb 0
scoreboard players set #pxS3 mb 0
scoreboard players set #pxS4 mb 0
scoreboard players set #pxS5 mb 0
scoreboard players set #pxS6 mb 0
scoreboard players set #pxS7 mb 0
scoreboard players set #pxS8 mb 0
scoreboard players set #pxS9 mb 0
scoreboard players set #pxS10 mb 0
scoreboard players set #pxS11 mb 0
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
data modify storage rlk:mboss push set value []
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] unless entity @s[tag=rlk_mb_inv] run function rlk:mboss/px/inv_on
