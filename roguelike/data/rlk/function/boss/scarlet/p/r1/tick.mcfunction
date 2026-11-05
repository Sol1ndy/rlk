# R1 자영 돌격: one pattern tick (#pt hr 1..76), dispatched by 16-tick blocks to k/<t>.
execute if score #pt hr matches 0..15 run return run function rlk:boss/scarlet/p/r1/b/0
execute if score #pt hr matches 16..31 run return run function rlk:boss/scarlet/p/r1/b/1
execute if score #pt hr matches 32..47 run return run function rlk:boss/scarlet/p/r1/b/2
execute if score #pt hr matches 48..63 run return run function rlk:boss/scarlet/p/r1/b/3
execute if score #pt hr matches 64..79 run return run function rlk:boss/scarlet/p/r1/b/4
