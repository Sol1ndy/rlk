# 증폭의 풀 (shells, id 33; plan 8.3). tick (#apq33T = the clip tick).
scoreboard players operation #apq33T mb = #apPT mb
scoreboard players operation #apq33T mb -= #apq33O mb
execute if score #apq33T mb matches 113.. run return run function rlk:boss/apep/p/shells/done
execute if score #apq33T mb matches 0..23 run return run function rlk:boss/apep/p/shells/kd/0_23
execute if score #apq33T mb matches 24..97 run return run function rlk:boss/apep/p/shells/kd/24_97
