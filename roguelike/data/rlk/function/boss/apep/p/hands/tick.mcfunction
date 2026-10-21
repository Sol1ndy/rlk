# P2 tick (#apPT = the hands clip tick; -9..0 the pre-turn)
execute if score #apPT mb matches 0..61 run return run function rlk:boss/apep/p/hands/kd/0_61
execute if score #apPT mb matches 62..140 run return run function rlk:boss/apep/p/hands/kd/62_140
