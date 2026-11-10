# @s = enemy with pips left (bal/mods). A burst hit (#burstDmg tmp = the game time of the burst's damage calc, set by
# items/hook/burst_dmg, cleared by char/after_hit) and a strong reaction (#rx tmp, element/react) take balance; their
# per-target windows make a multi-hit burst or a chain of reactions count once.
scoreboard players set #n bal 0
execute store result score #now bal run time query gametime
execute if score #burstDmg tmp = #now bal run function rlk:bal/src/burst
execute if score #rx tmp matches 1.. run function rlk:bal/src/rx
execute if score #n bal matches 1.. run function rlk:bal/take
