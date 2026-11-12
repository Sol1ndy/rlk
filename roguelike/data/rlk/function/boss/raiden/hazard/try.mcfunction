execute if score @s rdHMax matches 1.. if score @s rdHHit >= @s rdHMax run return 0
function rlk:boss/raiden/hazard/hit
execute if score #rdHit rd matches 1 run function rlk:boss/raiden/hazard/land
# Combat overhaul C: in the perfect-dodge window a dodgeable hazard that missed the body is tested again at the dodge's
# start (try_near; a contact there is judged as a perfect dodge).
execute if score #rdHit rd matches 0 if score #dgOpen cb matches 1 unless entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hazard/try_near
