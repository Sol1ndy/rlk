# Start group Q5 in p2 (@s = body).
execute if score #ai_q5 kn matches 46 run return run function rlk:boss/arlecchino/core/start/q5b
execute if score #ai_q5 kn matches 47 run return run function rlk:boss/arlecchino/core/start/q5a
execute store result score #t kn run random value 0..1
execute if score #t kn matches 1 run return run function rlk:boss/arlecchino/core/start/q5b
function rlk:boss/arlecchino/core/start/q5a
return 1
