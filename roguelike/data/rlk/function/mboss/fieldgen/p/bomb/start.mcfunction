# C1 일점 상쇄 (clip bomb_run, then slam at 58; @s = body, at it): route locked at 0, bombs 12..54 (strikes +6), the finisher re-lock and slam r 5 at 75, end 103.
scoreboard players set #fq1Pz mb 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:mboss/fieldgen/p/bomb/route
function rlk:mboss/fieldgen/rig_stub/face/track
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.5 0.9 0.17
