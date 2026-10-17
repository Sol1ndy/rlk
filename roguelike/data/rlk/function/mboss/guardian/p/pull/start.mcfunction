# P4 start (@s = body, player far): pull clip (40 t: aura 0, cage 11, relocate 32), then the swing clip
# 12 t after the relocation (51 t: swing1 20-24, swing2 33-39). Pull: undodgeable after the 32 t tell (K14).
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/pull
function rlk:mboss/guardian/voice/attack
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.3
playsound minecraft:entity.warden.sonic_charge hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.3
