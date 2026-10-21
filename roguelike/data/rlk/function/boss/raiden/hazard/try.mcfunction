execute if score @s rdHMax matches 1.. if score @s rdHHit >= @s rdHMax run return 0
function rlk:boss/raiden/hazard/hit
execute if score #rdHit rd matches 1 run function rlk:boss/raiden/hazard/land
