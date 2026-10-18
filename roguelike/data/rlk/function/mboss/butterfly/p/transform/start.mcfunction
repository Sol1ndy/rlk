# Transformation (core service pattern 20; clip transform, @s = body, at it): the cocoon glows, the wings
# open (4), the light sphere (6: 달빛 고치 + 달빛 이슬 via p/svc), ripple rings, full spread; end 30.
function rlk:mboss/butterfly/rig_stub/look/dendro
scoreboard players set #bfLook mb 7
function rlk:mboss/butterfly/rig_stub/face/player
particle minecraft:dust{color:[0.71f,0.941f,0.537f],scale:1.3} ~ ~1.0 ~ 0.3 0.7 0.3 0 10 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run function rlk:mboss/butterfly/fx/p/tf_sheath
function rlk:mboss/butterfly/fx/snd/transform_glow
