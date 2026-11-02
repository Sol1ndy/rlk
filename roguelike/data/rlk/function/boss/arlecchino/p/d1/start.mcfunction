# D1 블러드 돌진 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig/play/d1
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/embers_puff
execute at @s run function rlk:boss/arlecchino/fx/snd/dash_tell
