# Undodgeable (돌진, 수천수만의 염원, guard recovery): no dodge and no i-frames for this one hit (#hcND tmp 1, read by
# player/def/judge), and unparriable (land sets #hcNP).
scoreboard players set #hcND tmp 1
scoreboard players set #rdNoDodge rd 1
function rlk:boss/raiden/hurt
scoreboard players set #rdNoDodge rd 0
