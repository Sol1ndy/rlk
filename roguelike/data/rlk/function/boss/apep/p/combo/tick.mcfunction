# P6 tick (#apPT: combo_a 0-28, combo_b 29-72, combo_c / combo_end 73-92, combo_d / combo_end 93-)
execute if score #apPT mb matches 1..54 run return run function rlk:boss/apep/p/combo/kd/1_54
execute if score #apPT mb matches 55..170 run return run function rlk:boss/apep/p/combo/kd/55_170
