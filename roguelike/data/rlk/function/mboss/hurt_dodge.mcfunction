# A hit that did not land (#dodged 1): #mbDodgeEv +1; #mbDodgeOk 1 (the "perfect" event, e.g. Azhdaha's brand cleanse) only
# for a perfect dodge (#pdg tmp 1) or a perfect parry (#parT tmp 3) - not for i-frames (burst, revive, fall).
scoreboard players add #mbDodgeEv mb 1
execute if score #pdg tmp matches 1 run scoreboard players set #mbDodgeOk mb 1
execute if score #parT tmp matches 3 run scoreboard players set #mbDodgeOk mb 1
