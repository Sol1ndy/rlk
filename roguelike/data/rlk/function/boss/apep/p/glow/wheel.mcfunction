# @s = a homing wheel (module tick, before pj/all moves it; mbPjT = ticks flown): it peels off the carpet front toward the
# player from 2 t (<= 8 deg/t, level flight: the pitch stays 0) and slows to 0.5 b/t after 6 t on the
# front; the trail every 2 t (run as the wheel: it also spins the prop), the loop sound every 10 t.
execute if score @s mbPjT matches 6 run scoreboard players set @s mbPjV 5
execute if score @s mbPjT matches 2.. run function rlk:mboss/pj/steer {max:8}
execute at @s run tp @s ~ ~ ~ ~ 0
scoreboard players operation #apq3M mb = @s mbPjT
scoreboard players operation #apq3M mb %= #apK2 mb
execute if score #apq3M mb matches 0 run function rlk:boss/apep/fx/p/homing_trail
scoreboard players operation #apq3M mb = @s mbPjT
scoreboard players operation #apq3M mb %= #apK10 mb
execute if score #apq3M mb matches 1 run function rlk:boss/apep/fx/snd/p3_homing_loop
