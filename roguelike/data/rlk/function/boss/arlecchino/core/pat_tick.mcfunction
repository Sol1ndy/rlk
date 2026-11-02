# The running pattern (@s = body): #pt + 1, the core wrapper core/run/<key> (break window + p/<key>/tick).
scoreboard players add #pt kn 1
execute if score #pat kn matches 1 run function rlk:boss/arlecchino/core/run/a2
execute if score #pat kn matches 2 run function rlk:boss/arlecchino/core/run/a5
execute if score #pat kn matches 3 run function rlk:boss/arlecchino/core/run/b1
execute if score #pat kn matches 4 run function rlk:boss/arlecchino/core/run/b2
execute if score #pat kn matches 5 run function rlk:boss/arlecchino/core/run/c1
execute if score #pat kn matches 6 run function rlk:boss/arlecchino/core/run/c2
execute if score #pat kn matches 7 run function rlk:boss/arlecchino/core/run/d1
execute if score #pat kn matches 8 run function rlk:boss/arlecchino/core/run/d2
execute if score #pat kn matches 9 run function rlk:boss/arlecchino/core/run/e1
execute if score #pat kn matches 10 run function rlk:boss/arlecchino/core/run/f1
execute if score #pat kn matches 11 run function rlk:boss/arlecchino/core/run/g1
execute if score #pat kn matches 12 run function rlk:boss/arlecchino/core/run/h1
execute if score #pat kn matches 13 run function rlk:boss/arlecchino/core/run/a4
execute if score #pat kn matches 20 run function rlk:boss/arlecchino/core/run/e70
execute if score #done kn matches 1 run function rlk:boss/arlecchino/core/pat_end
