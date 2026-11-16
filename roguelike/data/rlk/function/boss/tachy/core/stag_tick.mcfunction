# G3 stagger countdown (@s = body); then the recovery.
scoreboard players remove #stag tk 1
execute if score #stag tk matches ..0 run function rlk:boss/tachy/core/stag_end
