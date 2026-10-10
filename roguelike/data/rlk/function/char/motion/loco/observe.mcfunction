# Centiblock displacement, not requested velocity: a wall stops the gait.
execute store result score #pmX tmp run data get entity @e[tag=rlk_av,limit=1] Pos[0] 100
execute store result score #pmZ tmp run data get entity @e[tag=rlk_av,limit=1] Pos[2] 100
scoreboard players operation #pmDX tmp = #pmX tmp
scoreboard players operation #pmDZ tmp = #pmZ tmp
scoreboard players operation #pmDX tmp -= @s pmPX
scoreboard players operation #pmDZ tmp -= @s pmPZ
execute unless score @s pmPosValid matches 1 run scoreboard players set #pmDX tmp 0
execute unless score @s pmPosValid matches 1 run scoreboard players set #pmDZ tmp 0
scoreboard players operation @s pmPX = #pmX tmp
scoreboard players operation @s pmPZ = #pmZ tmp
scoreboard players set @s pmPosValid 1
scoreboard players set #pmNeg tmp -1
execute if score #pmDX tmp matches ..-1 run scoreboard players operation #pmDX tmp *= #pmNeg tmp
execute if score #pmDZ tmp matches ..-1 run scoreboard players operation #pmDZ tmp *= #pmNeg tmp
scoreboard players operation #pmMove tmp = #pmDX tmp
scoreboard players operation #pmMove tmp > #pmDZ tmp
scoreboard players operation #pmMinor tmp = #pmDX tmp
scoreboard players operation #pmMinor tmp < #pmDZ tmp
# Ignore teleports; locomotion resumes from the next ordinary displacement.
execute if score #pmMove tmp matches 101.. run scoreboard players set #pmMinor tmp 0
execute if score #pmMove tmp matches 101.. run scoreboard players set #pmMove tmp 0
# max + 3/8 min approximates distance without slowing diagonal footsteps.
scoreboard players set #pmThree tmp 3
scoreboard players set #pmEight tmp 8
scoreboard players operation #pmMinor tmp *= #pmThree tmp
scoreboard players operation #pmMinor tmp /= #pmEight tmp
scoreboard players operation #pmMove tmp += #pmMinor tmp
scoreboard players set @s pmWantMode 0
execute if score #pmMove tmp matches 2.. if score #inAct view matches 1 run scoreboard players set @s pmWantMode 1
execute if score @s pmWantMode matches 1 if score #sprNow view matches 1 run scoreboard players set @s pmWantMode 2
execute if score @s dashMoveT matches 1.. run scoreboard players set @s pmWantMode 2
execute unless data entity @e[tag=rlk_av,limit=1] {OnGround:1b} run scoreboard players set @s pmWantMode 3
scoreboard players set @s pmLocSpeed 100
execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed = #pmMove tmp
execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed *= #100 tmp
scoreboard players set #pmStride tmp 20
execute if score @s pmWantMode matches 2 run scoreboard players set #pmStride tmp 30
execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed /= #pmStride tmp
execute if score @s pmLocSpeed matches ..49 run scoreboard players set @s pmLocSpeed 50
execute if score @s pmLocSpeed matches 201.. run scoreboard players set @s pmLocSpeed 200
