# @s = body: the second star broke inside the timer -> groggy (the 18 % hit lands 5 t later via star/bq2).
scoreboard players set #gdTim mb 0
scoreboard players set #gdTimS mb 0
scoreboard players set #gdHaze mb 0
function rlk:mboss/guardian/chaos/sigil_break
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs]
function rlk:mboss/guardian/rig/play/chaos_fall
function rlk:mboss/guardian/groggy/begin
