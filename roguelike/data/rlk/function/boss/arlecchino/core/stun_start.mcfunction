# The stun (@s = body): brk then stun / stun2 (140 t), hittable, the under-bar counts down.
function rlk:boss/arlecchino/core/stop_move
function rlk:boss/arlecchino/core/ground
function rlk:boss/arlecchino/core/looks_rest
scoreboard players set #pat kn 50
scoreboard players set #pt kn 0
scoreboard players set #stun kn 1
scoreboard players set #stun_t kn 160
tag @s add rlk_kn_stun
function rlk:boss/arlecchino/rig_stub/play/brk
function rlk:boss/arlecchino/hud/sub
