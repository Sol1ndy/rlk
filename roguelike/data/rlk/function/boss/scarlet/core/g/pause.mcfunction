# A gauntlet paused (@s = body): cancelled now; what resume does (#grs).
scoreboard players set #grs hr 1
execute if score #gres hr matches 1 run scoreboard players set #grs hr 3
execute if score #gres hr matches 2 if score #gk hr matches 2 run scoreboard players set #grs hr 2
function rlk:boss/scarlet/core/cancel_d
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/fx/hud/warn {on:0}
scoreboard players set #hrLook hr 2
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
