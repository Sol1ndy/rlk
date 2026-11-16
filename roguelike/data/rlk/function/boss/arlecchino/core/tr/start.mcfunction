# T: the P1 floor was reached (@s = body): the running pattern is cancelled, invulnerable + cine (player damage
# refused) throughout; the transition sequence (seq/t_p2 or the stand-in, 180 t); repool + music at 140.
function rlk:boss/arlecchino/core/cancel_d
function rlk:boss/arlecchino/core/win_off
kill @e[tag=rlk_kn_p]
scoreboard players set #fl kn 0
scoreboard players set #ph kn 4
scoreboard players set #pat kn 51
scoreboard players set #pt kn 0
scoreboard players set #sq kn 0
scoreboard players set #sqdone kn 0
scoreboard players set #trt kn 0
tag @s add rlk_mb_inv
function rlk:mboss/cine/start
function rlk:boss/arlecchino/core/stop_move
function rlk:boss/arlecchino/core/ground
function rlk:boss/arlecchino/core/looks_rest
function rlk:boss/arlecchino/seq/t_p2/start
function rlk:boss/arlecchino/hud/sub
