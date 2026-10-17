function rlk:mboss/d/tick
execute if score #mbSt mb matches 1 unless score #mbNoLeash mb matches 1 run function rlk:mboss/mv/leash
