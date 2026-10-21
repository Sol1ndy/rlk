# @s = body, #apTst = the requested test id (ap_contract 0.8; the phase jumps of 1.8).
execute if score #mbSt mb matches 0 run function rlk:mboss/apep/intro/done
scoreboard players set #apArg mb 0
execute if score #apTst mb matches 1 run return run function rlk:mboss/apep/test/p1_1
execute if score #apTst mb matches 2 run return run function rlk:mboss/apep/test/p1_2
execute if score #apTst mb matches 3 run return run function rlk:mboss/apep/test/p1_3
execute if score #apTst mb matches 4 run return run function rlk:mboss/apep/test/p1_4
execute if score #apTst mb matches 5 run return run function rlk:mboss/apep/test/p1_5
execute if score #apTst mb matches 6 run return run function rlk:mboss/apep/test/p1_6
execute if score #apTst mb matches 8 run return run function rlk:mboss/apep/test/r_p4
execute if score #apTst mb matches 9 run return run function rlk:mboss/apep/test/p6_4
execute if score #apTst mb matches 20 run return run function rlk:mboss/apep/test/t1
execute if score #apTst mb matches 21 run return run function rlk:mboss/apep/test/h_up
execute if score #apTst mb matches 22 run return run function rlk:mboss/apep/test/h_down
execute if score #apTst mb matches 23 run return run function rlk:mboss/apep/test/org_basic
execute if score #apTst mb matches 24 run return run function rlk:mboss/apep/test/org_guard
execute if score #apTst mb matches 25 run return run function rlk:mboss/apep/test/org_nest
execute if score #apTst mb matches 26 run return run function rlk:mboss/apep/test/org_nurt
execute if score #apTst mb matches 27 run return run function rlk:mboss/apep/test/org_pred
execute if score #apTst mb matches 28 run return run function rlk:mboss/apep/test/org_destr
execute if score #apTst mb matches 29 run return run function rlk:mboss/apep/test/timeout
execute if score #apTst mb matches 30 run return run function rlk:mboss/apep/test/cs_full
execute if score #apTst mb matches 60 run return run function rlk:mboss/apep/test/cs_only
execute if score #apTst mb matches 31 run return run function rlk:mboss/apep/test/p3_31
execute if score #apTst mb matches 33 run return run function rlk:mboss/apep/test/p3_33
execute if score #apTst mb matches 34 run return run function rlk:mboss/apep/test/p3_34
execute if score #apTst mb matches 35 run return run function rlk:mboss/apep/test/p3_35
execute if score #apTst mb matches 32 run return run function rlk:mboss/apep/test/p3_32
execute if score #apTst mb matches 37 run return run function rlk:mboss/apep/test/q2_lethal
execute if score #apTst mb matches 40 run return run function rlk:mboss/apep/test/fail1
execute if score #apTst mb matches 41 run return run function rlk:mboss/apep/test/fail2
execute if score #apTst mb matches 61 run return run function rlk:mboss/apep/test/stance
execute if score #apTst mb matches 99 run return run function rlk:mboss/apep/test/idle
function rlk:mboss/apep/test/help
