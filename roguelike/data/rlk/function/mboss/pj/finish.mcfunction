# Event 1/2 (non-returning) or 3 with #pjKeep 0 preset: removed unless the hook keeps it (released).
scoreboard players set #pjKeep mb 0
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 1 run return run function rlk:mboss/pj/release
kill @s
