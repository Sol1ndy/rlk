# Her hit events of the last tick (@s = body; the first line of a fight-phase tick; the framework's mboss/hurt_ev):
# #hpp = her hits that landed (a tier 1 / 2 parry is a landed hit), each charges the gauge; #pp = a perfect parry
# (#mbDodgeOk with #parT tmp 3; a perfect dodge is #parT 0). The events are cleared.
scoreboard players operation #hpp hr = #mbHitEv mb
execute unless score #hpp hr matches 1.. run scoreboard players set #hpp hr 0
scoreboard players set #pp hr 0
execute if score #mbDodgeOk mb matches 1 if score #parT tmp matches 3 run scoreboard players set #pp hr 1
scoreboard players set #mbHitEv mb 0
scoreboard players set #mbDodgeEv mb 0
scoreboard players set #mbDodgeOk mb 0
execute if score #hpp hr matches 1.. run function rlk:boss/scarlet/core/gauge/hit
