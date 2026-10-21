# Hook pj_end (@s = a P3 prop, #pjEv 1 wall / 2 life over / 4 hit): a hit pops the wheel where it is (wheel_pop + the
# thorn sound); a wheel that ran out fizzles (the one-card spark + gold-orange dust; perf, AP-I2: slam 1's wheels run out
# on t163 = slam 2's carpet tick, which passed 3000 commands with two full pops in the natural-fight probe).
execute if score #pjEv mb matches 4 at @s run function rlk:boss/apep/fx/snd/p3_wheel_hit
execute if score #pjEv mb matches 4 at @s run function rlk:boss/apep/fx/p/wheel_pop
execute unless score #pjEv mb matches 4 at @s run function rlk:boss/apep/fx/p/spark
execute unless score #pjEv mb matches 4 at @s run particle minecraft:dust{color:[0.91f,0.565f,0.165f],scale:1.2} ~ ~ ~ 0.4 0.4 0.4 0 6 force @a[tag=player]
scoreboard players set #pjKeep mb 0
