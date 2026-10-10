scoreboard objectives add pmActive dummy
scoreboard objectives add pmTick dummy
scoreboard objectives add pmLen dummy
scoreboard objectives add pmChar dummy
scoreboard objectives add pmSpeed dummy
scoreboard objectives add pmAcc dummy
scoreboard objectives add pmStep dummy
scoreboard objectives add pmVisible dummy
scoreboard objectives add pmRigChar dummy
scoreboard objectives add pmLocMode dummy
scoreboard objectives add pmWantMode dummy
scoreboard objectives add pmLocT dummy
scoreboard objectives add pmLocAcc dummy
scoreboard objectives add pmLocSpeed dummy
scoreboard objectives add pmBlend dummy
scoreboard objectives add pmPX dummy
scoreboard objectives add pmPZ dummy
scoreboard objectives add pmPosValid dummy
scoreboard objectives add pmWeapon dummy
scoreboard objectives add pmWantW dummy
execute as @a[tag=player] run function rlk:char/motion/stop
kill @e[tag=rlk_pm]
kill @e[tag=rlk_pm_basis]
