# From the top of combat/apply (@s = a hit proxy, at it). One attack event = one hit on the body (cm.md 9.6): a second
# hit in the same game tick with the same #atkSeq is swallowed (no number, no reaction); else the hit is re-run as the
# body at the proxy (the number shows here) with #pxIn 1, and #mbPart / #mbPartGT record the proxy.
execute store result score #pxG mb run time query gametime
execute if score #pxG mb = #pxGT mb if score #atkSeq tmp = #pxSeq mb run return 0
scoreboard players operation #pxGT mb = #pxG mb
scoreboard players operation #pxSeq mb = #atkSeq tmp
scoreboard players operation #mbPart mb = @s mbPart
scoreboard players operation #mbPartGT mb = #pxG mb
scoreboard players set #pxIn mb 1
execute at @s as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:combat/apply
scoreboard players set #pxIn mb 0
return 1
