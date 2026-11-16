# 생명의 나선 (spiral, id 35; plan 8.3). tick (#apq35T = the clip tick).
scoreboard players operation #apq35T mb = #apPT mb
scoreboard players operation #apq35T mb -= #apq35O mb
execute if score #apq35T mb matches 72.. run return run function rlk:boss/apep/p/spiral/done
execute if score #apq35T mb matches 0..26 run return run function rlk:boss/apep/p/spiral/kd/0_26
execute if score #apq35T mb matches 27..65 run return run function rlk:boss/apep/p/spiral/kd/27_65
