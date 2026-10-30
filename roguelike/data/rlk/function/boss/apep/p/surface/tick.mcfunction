# 수면 포격 (surface, id 36; plan 8.3). tick (#apq36T = the pattern tick after the prelude).
scoreboard players operation #apq36T mb = #apPT mb
scoreboard players operation #apq36T mb -= #apq36O mb
execute if score #apq36T mb matches 90.. run return run function rlk:boss/apep/p/surface/done
execute if score #apq36T mb matches 0..28 run return run function rlk:boss/apep/p/surface/kd/0_28
execute if score #apq36T mb matches 29..49 run return run function rlk:boss/apep/p/surface/kd/29_49
