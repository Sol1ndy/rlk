# 이동 돌진 (mstrike, id 31; plan 8.3). tick (#apq31T = the clip tick).
scoreboard players operation #apq31T mb = #apPT mb
scoreboard players operation #apq31T mb -= #apq31O mb
execute if score #apq31T mb matches 92.. run return run function rlk:boss/apep/p/mstrike/done
execute if score #apq31T mb matches 0..35 run return run function rlk:boss/apep/p/mstrike/kd/0_35
execute if score #apq31T mb matches 36..72 run return run function rlk:boss/apep/p/mstrike/kd/36_72
