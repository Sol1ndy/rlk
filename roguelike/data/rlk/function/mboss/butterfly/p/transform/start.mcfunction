# Transformation (core service pattern 20; clip transform, @s = body, at it): the cocoon glows, the wings
# open (4), the light sphere (6: 달빛 고치 + 달빛 이슬 via p/svc), ripple rings, full spread; end 30.
function rlk:mboss/butterfly/rig_stub/look/dendro
scoreboard players set #bfLook mb 7
function rlk:mboss/butterfly/rig_stub/face/player
particle minecraft:dust{color:[0.71f,0.941f,0.537f],scale:1.3} ~ ~1.0 ~ 0.3 0.7 0.3 0 10 force @a[tag=player]
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.27
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
