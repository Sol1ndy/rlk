# P4 start (@s = body, player far): pull clip (aura 0, cage 11, relocate 32), voice line, hiss + charge.
scoreboard players set #gp4Ok mb 0
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/pull
function rlk:mboss/guardian/voice/attack
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.23
