# Arena rim, the safe circle (green) and a ring growing from the centre.
execute positioned 200 ~ 8 run function rlk:mboss/hz/p/c/42 with storage rlk:mboss hzp
$execute positioned 200 ~ 8 run function rlk:mboss/hz/p/c/$(kp) with storage rlk:mboss hzp
execute if score @s mbHzR0 matches 1.. run function rlk:mboss/hz/d/full_safe
