# Start C3 (@s = body): farther than 5.5 b -> the gap closer first (core/close), else at once.
function rlk:mboss/mv/dist
execute if score #mbDist mb matches 56.. run return run function rlk:boss/tachy/core/close/start {q:7}
function rlk:boss/tachy/core/begin/c3
