# A6 후방 섬보 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
function rlk:boss/scarlet/rig/play/a6
function rlk:boss/scarlet/p/a6/blink
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run function rlk:boss/scarlet/fx/p/blink_bubble
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/a6_blink
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:120}
