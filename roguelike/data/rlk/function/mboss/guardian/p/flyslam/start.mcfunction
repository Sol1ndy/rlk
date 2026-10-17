# P5 하늘을 심판하는 자 start (@s = body, player far): flyslam clip (101 t). See p56.py for the timeline.
kill @e[tag=rlk_mb_gd_p5]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/guardian/rig/play/flyslam
