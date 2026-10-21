# @s = body. First tick of the main-slot pattern #apPid: clock -lead (0 for most), its first clip at clock 0,
# start; a service started at #apReqT >= 1 (tests) resumes through its reload at that clock.
scoreboard players set #apPNew mb 0
scoreboard players set #apPT mb 0
scoreboard players set #apPEnd mb 0
scoreboard players set #apPRel mb 0
scoreboard players set #apPMax mb 400
scoreboard players set #apPLen mb 400
execute if score #apPid mb matches 1 run scoreboard players set #apPMax mb 100
execute if score #apPid mb matches 2 run scoreboard players set #apPMax mb 170
execute if score #apPid mb matches 3 run scoreboard players set #apPMax mb 260
execute if score #apPid mb matches 4 run scoreboard players set #apPMax mb 150
execute if score #apPid mb matches 5 run scoreboard players set #apPMax mb 150
execute if score #apPid mb matches 6 run scoreboard players set #apPMax mb 200
execute if score #apPid mb matches 7 run scoreboard players set #apPMax mb 60
execute if score #apPid mb matches 31 run scoreboard players set #apPMax mb 120
execute if score #apPid mb matches 33 run scoreboard players set #apPMax mb 130
execute if score #apPid mb matches 34 run scoreboard players set #apPMax mb 135
execute if score #apPid mb matches 35 run scoreboard players set #apPMax mb 90
execute if score #apPid mb matches 36 run scoreboard players set #apPMax mb 110
execute if score #apPid mb matches 32 run scoreboard players set #apPMax mb 312
execute if score #apPid mb matches 20 run scoreboard players set #apPMax mb 140
execute if score #apPid mb matches 40 run scoreboard players set #apPMax mb 64
execute if score #apPid mb matches 60 run scoreboard players set #apPMax mb 196
execute if score #apPid mb matches 10 run scoreboard players set #apPMax mb 80
execute if score #apPid mb matches 61 run scoreboard players set #apPMax mb 20
execute if score #apPid mb matches 1 run scoreboard players set #apPLen mb 82
execute if score #apPid mb matches 2 run scoreboard players set #apPLen mb 140
execute if score #apPid mb matches 3 run scoreboard players set #apPLen mb 225
execute if score #apPid mb matches 4 run scoreboard players set #apPLen mb 130
execute if score #apPid mb matches 5 run scoreboard players set #apPLen mb 127
execute if score #apPid mb matches 6 run scoreboard players set #apPLen mb 170
execute if score #apPid mb matches 7 run scoreboard players set #apPLen mb 42
execute if score #apPid mb matches 31 run scoreboard players set #apPLen mb 92
execute if score #apPid mb matches 33 run scoreboard players set #apPLen mb 113
execute if score #apPid mb matches 34 run scoreboard players set #apPLen mb 95
execute if score #apPid mb matches 35 run scoreboard players set #apPLen mb 72
execute if score #apPid mb matches 36 run scoreboard players set #apPLen mb 90
execute if score #apPid mb matches 32 run scoreboard players set #apPLen mb 282
execute if score #apPid mb matches 20 run scoreboard players set #apPLen mb 136
execute if score #apPid mb matches 40 run scoreboard players set #apPLen mb 60
execute if score #apPid mb matches 60 run scoreboard players set #apPLen mb 192
execute if score #apPid mb matches 10 run scoreboard players set #apPLen mb 72
execute if score #apPid mb matches 61 run scoreboard players set #apPLen mb 16
execute if score #apPid mb matches 2 run scoreboard players set #apPT mb -10
execute if score #apPid mb matches 6 run scoreboard players set #apPT mb -10
execute if score #apReqT mb matches 1.. run return run function rlk:boss/apep/p/resume_at
scoreboard players set #apHudQ mb 1
execute if score #apPT mb matches 0 run function rlk:boss/apep/p/clip_d
function rlk:boss/apep/p/start_d
