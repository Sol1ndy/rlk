# Start group A in p1b (@s = body).
execute store result score #t kn run random value 1..100
execute if score #t kn matches ..50 run return run function rlk:boss/arlecchino/core/start/a5
function rlk:boss/arlecchino/core/start/a4
return 1
