# One tick before the cut: the crescent waves (they launch next tick, as the blade crosses her facing);
# one hit max for the whole volley.
scoreboard players add #rdGrpSerial rd 1
execute as @e[tag=rlk_rd_illusion] at @s rotated as @s run function rlk:boss/raiden/illusion/fire
function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"cross_d",d:1,look:"dark"}
