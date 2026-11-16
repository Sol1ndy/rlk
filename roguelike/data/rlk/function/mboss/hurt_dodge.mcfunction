# A hit that did not land (#dodged 1): #mbDodgeEv +1; #mbDodgeOk 1 (the "perfect" event, e.g. Azhdaha's brand cleanse) only
# for a perfect dodge (#pdg tmp 1) or a perfect parry (#parT tmp 3) - not for i-frames (burst, revive, fall) - of a real
# attack: not of a re-arming (lingering) hazard. (Before combat overhaul C: a dash-dodged projectile or one-shot hazard
# with a tell >= 12 t; the timing judge replaces the tell rule.)
scoreboard players add #mbDodgeEv mb 1
execute unless score #pdg tmp matches 1 unless score #parT tmp matches 3 run return 0
execute if score #mbSrcIn mb matches 1 if score @s mbHzRA matches 1.. run return 0
scoreboard players set #mbDodgeOk mb 1
