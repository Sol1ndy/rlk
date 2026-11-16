# @s (a spot marker or the body) on the floor: when its spot fails mv/ok (outside the safe disc, in a block), walk
# it 0.5 b toward the arena centre until it passes (at most 60 steps; #w1_n tk counts). Fails when none passed.
execute at @s if function rlk:mboss/mv/ok run return 1
execute if score #w1_n tk matches 60.. run return fail
scoreboard players add #w1_n tk 1
execute at @s unless function rlk:mboss/mv/ok facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
return run function rlk:boss/tachy/p/w1/u/fit
