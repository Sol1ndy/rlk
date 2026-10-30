# rlk_cmrot += #oUp (x100) in y, then clamped into this bird's box (x/z) and under its ceiling (y)
execute store result score #ox tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[0] 100
execute store result score #oy tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[1] 100
execute store result score #oz tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[2] 100
scoreboard players operation #oy tmp += #oUp tmp
scoreboard players operation #ox tmp > @s cmAX
scoreboard players operation #ox tmp < @s cmVx
scoreboard players operation #oz tmp > @s cmAZ
scoreboard players operation #oz tmp < @s cmVz
scoreboard players operation #oy tmp < @s cmVy
execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[0] double 0.01 run scoreboard players get #ox tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[1] double 0.01 run scoreboard players get #oy tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[2] double 0.01 run scoreboard players get #oz tmp
