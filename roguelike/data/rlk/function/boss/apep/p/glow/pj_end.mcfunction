# Hook pj_end (@s = a P3 prop, #pjEv 1 wall / 2 life over / 4 hit): the wheel pops where it is (a hit: the thorn sound).
execute if score #pjEv mb matches 4 at @s run function rlk:boss/apep/fx/snd/p3_wheel_hit
execute at @s run function rlk:boss/apep/fx/p/wheel_pop
scoreboard players set #pjKeep mb 0
