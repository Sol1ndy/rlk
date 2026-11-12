# H1 연옥 그림자 분신 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig/play/h1
function rlk:boss/arlecchino/p/h1/web
execute at @s run function rlk:boss/arlecchino/fx/snd/leap
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3 ~ run function rlk:boss/arlecchino/fx/p/threads {r:10}
