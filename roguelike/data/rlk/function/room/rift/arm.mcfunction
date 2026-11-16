# @s = the zone marker (rift/roll): the special of this rift (mboss/sp/roll: the test's fixed id first), zone tag
# rlk_riftz + data.rift {id}, at most once per run (#riftUsed 1: it counts even if never entered), the force spent,
# and mboss/sp/prep {id} (the special's arena forceloaded, its build job started now). No special: no rift.
scoreboard players set #riftForce room 0
execute unless function rlk:mboss/sp/roll run return 0
tag @s add rlk_riftz
scoreboard players set #riftUsed room 1
data modify entity @s data.rift set value {}
data modify entity @s data.rift.id set from storage rlk:mboss spid
function rlk:mboss/sp/prep with entity @s data.rift
