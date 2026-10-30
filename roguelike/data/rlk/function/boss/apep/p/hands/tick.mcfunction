# P2 tick (#apPT = the hands clip tick; -9..0 the pre-turn)
execute if score #apPT mb matches 0..33 run return run function rlk:boss/apep/p/hands/kd/0_33
execute if score #apPT mb matches 36..140 run return run function rlk:boss/apep/p/hands/kd/36_140
