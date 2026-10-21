# One tick before the volley: the slabs (they launch next tick); one hit max for the set.
scoreboard players add #rdGrpSerial rd 1
execute as @e[tag=rlk_rd_illusion] at @s rotated as @s run function rlk:boss/raiden/illusion/fire
