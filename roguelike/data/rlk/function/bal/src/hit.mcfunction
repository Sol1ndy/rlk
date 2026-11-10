# @s = enemy with pips left, after combat/apply took its HP (it survived; not true damage). A burst hit (#burstDmg tmp,
# set by items/hook/burst_dmg) and a strong reaction (#rx tmp, element/react) take balance; their per-target windows
# make a multi-hit burst or a chain of reactions count once.
execute unless score #burstDmg tmp matches 1 unless score #rx tmp matches 1.. run return 0
execute if score @s grgT matches 1.. run return 0
scoreboard players set #n bal 0
execute store result score #now bal run time query gametime
execute if score #burstDmg tmp matches 1 run function rlk:bal/src/burst
execute if score #rx tmp matches 1.. run function rlk:bal/src/rx
execute if score #n bal matches 1.. run function rlk:bal/take
