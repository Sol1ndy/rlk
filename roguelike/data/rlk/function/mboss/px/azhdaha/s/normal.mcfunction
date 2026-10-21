# State set "normal" of azhdaha: membership, live / parked, the push capsules (tenths, anchor frame), the rig
# visibility, the inv rule (rlk_mb_inv only through rlk_mb_pxinv: an inv the body already has is never touched).
data modify storage rlk:mboss px.set set value "normal"
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
scoreboard players set #pxS12 mb 1
function rlk:mboss/px/azhdaha/ev/1
function rlk:mboss/px/azhdaha/ev/2
function rlk:mboss/px/azhdaha/ev/3
function rlk:mboss/px/azhdaha/ev/4
function rlk:mboss/px/azhdaha/ev/5
function rlk:mboss/px/azhdaha/ev/6
function rlk:mboss/px/azhdaha/ev/7
function rlk:mboss/px/azhdaha/ev/8
function rlk:mboss/px/azhdaha/ev/9
function rlk:mboss/px/azhdaha/ev/10
function rlk:mboss/px/azhdaha/ev/11
function rlk:mboss/px/azhdaha/ev/12
data modify storage rlk:mboss push set value [{f0:-38,f1:26,hw:28,px:"",top:0},{f0:26,f1:54,hw:16,px:"head",top:35}]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/azhdaha/rig/state/normal
execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1] run function rlk:mboss/px/inv_off
