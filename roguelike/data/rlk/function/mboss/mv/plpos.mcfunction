# (anywhere; cm.md 13.2, CM-REVIEW PERF-4) #mbPX / #mbPZ mb = the player's body x / z in milliblocks, read from the body
# (a player: every entity NBT read saves the whole player) once per game tick, in one read (Pos -> rlk:mboss plp); later
# calls in the same tick reuse it. Fails when there is no body. A chapter-runtime teleport of the player in the tick
# (push/capsule, the chapter arena's tp_in) sets #mbPlG -1, so the next call reads again.
execute store result score #plG mb run time query gametime
execute if score #plG mb = #mbPlG mb run return 1
execute unless entity @e[tag=rlk_body,limit=1] run return fail
data modify storage rlk:mboss plp set from entity @e[tag=rlk_body,limit=1] Pos
execute store result score #mbPX mb run data get storage rlk:mboss plp[0] 1000
execute store result score #mbPZ mb run data get storage rlk:mboss plp[2] 1000
scoreboard players operation #mbPlG mb = #plG mb
return 1
