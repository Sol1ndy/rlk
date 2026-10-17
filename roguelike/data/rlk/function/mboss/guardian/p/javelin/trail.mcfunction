# @s = body, at A rotated along the lane: the fading trail, a step every 1 b.
particle minecraft:dust_color_transition{from_color:[0.78f,0.675f,0.341f],to_color:[0.624f,0.478f,0.196f],scale:1.1} ~ ~ ~ 0.06 0.06 0.1 0 1 force @a[tag=player]
scoreboard players add #gp2S mb 10
execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^1 run function rlk:mboss/guardian/p/javelin/trail
