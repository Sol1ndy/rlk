# From combat/apply (@s = a rlk_mb_big body hit directly, #pxIn 0, not true damage): the same de-dupe as px/hit with
# #mbPart 0. Returns 1 = go on with the hit, fail = swallow it (the same attack already hit through a proxy).
execute store result score #pxG mb run time query gametime
execute if score #pxG mb = #pxGT mb if score #atkSeq tmp = #pxSeq mb run return fail
scoreboard players operation #pxGT mb = #pxG mb
scoreboard players operation #pxSeq mb = #atkSeq tmp
scoreboard players set #mbPart mb 0
scoreboard players operation #mbPartGT mb = #pxG mb
return 1
