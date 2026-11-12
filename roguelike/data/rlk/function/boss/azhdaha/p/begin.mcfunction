# @s = body. First tick of the main-slot pattern #azPat: clock -lead (0 for most), the clip at clock 0, start;
# a service started at #azReqT >= 1 (tests 25 / 61) resumes through its reload instead.
scoreboard players set #azPNew mb 0
scoreboard players set #azPT mb 0
scoreboard players set #azPEnd mb 0
scoreboard players set #azPRel mb 0
scoreboard players set #azPMax mb 200
scoreboard players set #azPLen mb 200
execute if score #azPat mb matches 1 run scoreboard players set #azPMax mb 80
execute if score #azPat mb matches 2 run scoreboard players set #azPMax mb 70
execute if score #azPat mb matches 3 run scoreboard players set #azPMax mb 90
execute if score #azPat mb matches 4 run scoreboard players set #azPMax mb 100
execute if score #azPat mb matches 5 run scoreboard players set #azPMax mb 80
execute if score #azPat mb matches 10 run scoreboard players set #azPMax mb 100
execute if score #azPat mb matches 6 run scoreboard players set #azPMax mb 60
execute if score #azPat mb matches 7 run scoreboard players set #azPMax mb 80
execute if score #azPat mb matches 8 run scoreboard players set #azPMax mb 85
execute if score #azPat mb matches 9 run scoreboard players set #azPMax mb 320
execute if score #azPat mb matches 31 run scoreboard players set #azPMax mb 90
execute if score #azPat mb matches 32 run scoreboard players set #azPMax mb 110
execute if score #azPat mb matches 41 run scoreboard players set #azPMax mb 433
execute if score #azPat mb matches 42 run scoreboard players set #azPMax mb 433
execute if score #azPat mb matches 43 run scoreboard players set #azPMax mb 50
execute if score #azPat mb matches 44 run scoreboard players set #azPMax mb 170
execute if score #azPat mb matches 45 run scoreboard players set #azPMax mb 110
execute if score #azPat mb matches 46 run scoreboard players set #azPMax mb 150
execute if score #azPat mb matches 20 run scoreboard players set #azPMax mb 249
execute if score #azPat mb matches 21 run scoreboard players set #azPMax mb 182
execute if score #azPat mb matches 22 run scoreboard players set #azPMax mb 140
execute if score #azPat mb matches 23 run scoreboard players set #azPMax mb 439
execute if score #azPat mb matches 27 run scoreboard players set #azPMax mb 64
execute if score #azPat mb matches 28 run scoreboard players set #azPMax mb 60
execute if score #azPat mb matches 30 run scoreboard players set #azPMax mb 88
execute if score #azPat mb matches 1 run scoreboard players set #azPLen mb 65
execute if score #azPat mb matches 2 run scoreboard players set #azPLen mb 53
execute if score #azPat mb matches 3 run scoreboard players set #azPLen mb 71
execute if score #azPat mb matches 4 run scoreboard players set #azPLen mb 90
execute if score #azPat mb matches 5 run scoreboard players set #azPLen mb 63
execute if score #azPat mb matches 10 run scoreboard players set #azPLen mb 85
execute if score #azPat mb matches 6 run scoreboard players set #azPLen mb 50
execute if score #azPat mb matches 7 run scoreboard players set #azPLen mb 64
execute if score #azPat mb matches 8 run scoreboard players set #azPLen mb 70
execute if score #azPat mb matches 9 run scoreboard players set #azPLen mb 273
execute if score #azPat mb matches 31 run scoreboard players set #azPLen mb 82
execute if score #azPat mb matches 32 run scoreboard players set #azPLen mb 94
execute if score #azPat mb matches 41 run scoreboard players set #azPLen mb 429
execute if score #azPat mb matches 42 run scoreboard players set #azPLen mb 429
execute if score #azPat mb matches 43 run scoreboard players set #azPLen mb 34
execute if score #azPat mb matches 44 run scoreboard players set #azPLen mb 143
execute if score #azPat mb matches 45 run scoreboard players set #azPLen mb 88
execute if score #azPat mb matches 46 run scoreboard players set #azPLen mb 140
execute if score #azPat mb matches 20 run scoreboard players set #azPLen mb 243
execute if score #azPat mb matches 21 run scoreboard players set #azPLen mb 176
execute if score #azPat mb matches 22 run scoreboard players set #azPLen mb 134
execute if score #azPat mb matches 23 run scoreboard players set #azPLen mb 433
execute if score #azPat mb matches 27 run scoreboard players set #azPLen mb 60
execute if score #azPat mb matches 28 run scoreboard players set #azPLen mb 56
execute if score #azPat mb matches 30 run scoreboard players set #azPLen mb 82
execute if score #azPat mb matches 1 run scoreboard players set #azPT mb -8
execute if score #azPat mb matches 3 run scoreboard players set #azPT mb -10
execute if score #azReqT mb matches 1.. run return run function rlk:boss/azhdaha/p/resume_at
scoreboard players set #azHudQ mb 1
execute if score #azPT mb matches 0 run function rlk:boss/azhdaha/p/clip_d
function rlk:boss/azhdaha/p/start_d
