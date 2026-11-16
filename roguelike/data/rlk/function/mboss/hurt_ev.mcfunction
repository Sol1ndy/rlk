# @s = the attacker of a mboss/hurt call that reached the player (cm.md 13.3). Landed: #mbHitEv +1 with its element,
# shield-before-the-hit, re-arming / lingering source (#hzRearm hazard) and source kind (1 hazard, 2 projectile, 3 direct).
# Dodged: #mbDodgeEv +1; #mbDodgeOk 1 only for a one-shot strike hazard (no re-arm, tell >= 12 t, dodgeable) or a projectile.
execute if score #dodged tmp matches 1 run return run function rlk:mboss/hurt_dodge
scoreboard players add #mbHitEv mb 1
scoreboard players operation #mbHitEl mb = #cmEl tmp
scoreboard players operation #mbHitSh mb = #mbShIn mb
scoreboard players set #mbHitRA mb 0
execute if score #mbSrcIn mb matches 1 if score @s mbHzRA matches 1.. run scoreboard players set #mbHitRA mb 1
scoreboard players set #mbHitSrc mb 3
execute if score #mbSrcIn mb matches 1..2 run scoreboard players operation #mbHitSrc mb = #mbSrcIn mb
