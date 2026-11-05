# R2 pattern tick 42.
execute if score #r2_two hr matches 1 run function rlk:mboss/mv/face
execute if score #r2_two hr matches 1 run function rlk:boss/scarlet/g/disc/throw {kb:2}
execute if score #r2_two hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/disc_release
execute if score #r2_two hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/disc_fly
execute unless score #r2_two hr matches 1 run function rlk:mboss/mv/turn {max:10}
