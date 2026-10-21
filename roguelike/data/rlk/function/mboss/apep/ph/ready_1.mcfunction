# @s = body: phase 1 ready (tests): the stage gone, unparked at its place, p1 look, CROUCH, pool 53 %, floor 1 %.
function rlk:mboss/apep/ph/cut
function rlk:mboss/apep/rev/clear
function rlk:mboss/apep/org/clear
function rlk:mboss/apep/wall/clear
execute if score #apPark mb matches 1 run function rlk:mboss/apep/svc/unpark
execute unless score #mbPoolPct mb matches 53 run function rlk:mboss/apep/svc/repool_p1
function rlk:mboss/apep/svc/look_p1
function rlk:mboss/apep/rig_stub/stance/crouch
function rlk:mboss/apep/play/idle_p1
function rlk:mboss/apep/svc/phase_1
function rlk:mboss/apep/px/p1
function rlk:mboss/apep/heart/p1_respawn
scoreboard players set #apCool mb 10
execute unless score #mbMusPh mb matches 1 run function rlk:mboss/apep/svc/music_1
