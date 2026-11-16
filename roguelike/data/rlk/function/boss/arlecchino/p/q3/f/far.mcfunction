# Q3 far: two crescents +-6 deg at the player (one volley group).
function rlk:mboss/grp_new
scoreboard players operation #q3_g kn = #mbGrp mb
function rlk:boss/arlecchino/p/q3/f/cres_r6_kb3
function rlk:boss/arlecchino/p/q3/f/cres_l6_kb3
execute at @s run function rlk:boss/arlecchino/fx/snd/crescent_throw
