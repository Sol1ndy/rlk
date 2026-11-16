# The player stayed farther than 5.5 b for 20 t: 60 % a melee chain of this phase
# behind the gap-closer blink (core/start: farther than the gate), else the weighted pick. Fails when not taken.
execute store result score #t tk run random value 1..100
execute if score #t tk matches 61.. run return fail
return run function rlk:boss/tachy/ai/oor_go
