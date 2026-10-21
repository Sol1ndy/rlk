# World: as each hazard at its origin and frozen yaw. #rdRel = ticks since the hit / launch (negative before).
scoreboard players add @s rdHAge 1
execute if score @s rdHAge >= @s rdHLife run return run function rlk:boss/raiden/hazard/expire
scoreboard players operation #rdRel rd = @s rdHAge
scoreboard players operation #rdRel rd -= @s rdWind
# S3-F perf (review RD-P1): a travelling hazard whose hit is spent (it hit, or its front passed the body) only
# waits for its expiry (post: front past `reach`); its cards fly on by interpolation.
execute if score @s rdHHit matches 1.. if score @s rdHMax matches 1.. if score @s rdHK matches 5..7 if score @s rdHHit >= @s rdHMax if score #rdRel rd <= @s rdHF run return 0
# S3-F perf: a slab whose front is still well short of the body waits until it could reach it (k/slab_wait).
execute if score @s rdHNx > @s rdHAge if score #rdRel rd <= @s rdHF run return 0
execute if score @s rdHK matches 8 run function rlk:boss/raiden/hazard/k/follow_move
execute if score #rdRel rd matches ..-1 run return run function rlk:boss/raiden/hazard/pre
execute if score #rdRel rd matches 0 run return run function rlk:boss/raiden/hazard/fire
function rlk:boss/raiden/hazard/post
