# @s = body: the run ends (lane end / r 12 / 24 t): the hit goes, charge_stop (21 t), the
# skid (decelerating slide, turn <= 30 deg), the end tick; the dangerous part is over (release).
scoreboard players set #aq3R mb 0
scoreboard players set #aq3K mb 1
scoreboard players set #aq3H mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p3h] at @s rotated as @s run function rlk:mboss/hz/expire
scoreboard players operation #aq3E mb = #azPT mb
scoreboard players add #aq3E mb 21
scoreboard players operation #azPLen mb = #aq3E mb
function rlk:mboss/azhdaha/rig/play/charge_stop
execute at @s run function rlk:mboss/azhdaha/fx/p/skid
execute at @s run function rlk:mboss/azhdaha/fx/snd/charge_skid
function rlk:mboss/azhdaha/p/release
