# Q3 far: two crescents +-6 deg at the player (one volley group).
function rlk:mboss/grp_new
scoreboard players operation #q3_g kn = #mbGrp mb
function rlk:boss/arlecchino/p/q3/f/cres_r6_kb3
function rlk:boss/arlecchino/p/q3/f/cres_l6_kb3
execute at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
