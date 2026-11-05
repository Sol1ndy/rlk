# R2 월륜 일섬: one pattern tick (#pt hr 1..60), dispatched by 16-tick blocks to k/<t>.
execute if score #pt hr matches 0..15 run return run function rlk:boss/scarlet/p/r2/b/0
execute if score #pt hr matches 16..31 run return run function rlk:boss/scarlet/p/r2/b/1
execute if score #pt hr matches 32..47 run return run function rlk:boss/scarlet/p/r2/b/2
execute if score #pt hr matches 48..63 run return run function rlk:boss/scarlet/p/r2/b/3
