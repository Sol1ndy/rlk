# Contact: on the stop, facing the Heart; destr_fuse (56 t) -> destr_suck (5) -> the blast at contact + 61:
# the blast disc r 3.6 (quiet, made now with its 61 t tell; the fuse is the tell), the primed sound, the first pulse.
tp @s @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,sort=nearest,limit=1]
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
scoreboard players set @s apS 2
scoreboard players set @s apT 0
function rlk:boss/apep/om/destr/play/destr_fuse
execute at @s run function rlk:boss/apep/fx/snd/o7_primed
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
scoreboard players operation #apX mb = @s apL
execute at @s positioned ~ 201 ~ run function rlk:boss/apep/org/destr/hz
