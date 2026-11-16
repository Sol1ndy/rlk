# @s = body: phase 1 ready (tests): the stage gone, unparked at its place, p1 look, CROUCH, pool 53 %, floor 1 %.
function rlk:boss/apep/ph/cut
function rlk:boss/apep/rev/clear
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
execute if score #apPark mb matches 1 run function rlk:boss/apep/svc/unpark
execute unless score #mbPoolPct mb matches 53 run function rlk:boss/apep/svc/repool_p1
function rlk:boss/apep/svc/look_p1
function rlk:boss/apep/rig/stance/crouch
function rlk:boss/apep/play/idle_p1
function rlk:boss/apep/svc/phase_1
function rlk:boss/apep/px/p1
function rlk:boss/apep/heart/p1_respawn
scoreboard players set #apCool mb 10
execute unless score #mbMusPh mb matches 1 run function rlk:boss/apep/svc/music_1
