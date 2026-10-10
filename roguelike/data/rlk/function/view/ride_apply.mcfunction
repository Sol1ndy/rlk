# 받침 크기·카메라 거리 적용(rlk:view ride {d, s}). 카메라 거리 속성 = d ÷ s (바닐라가 탈것 크기를 곱함)
execute store result score #rs view run data get storage rlk:view ride.s 1000
execute store result score #rd view run data get storage rlk:view ride.d 1000
execute if score #rs view matches ..99 run scoreboard players set #rs view 100
scoreboard players operation #rd view *= #1000 tmp
scoreboard players operation #rd view /= #rs view
function rlk:view/burst_camera_scale
scoreboard players operation #rd view *= #bcMul view
scoreboard players operation #rd view /= #100 tmp
execute store result storage rlk:view rv.s double 0.001 run scoreboard players get #rs view
execute store result storage rlk:view rv.d double 0.001 run scoreboard players get #rd view
function rlk:view/ride_apply2 with storage rlk:view rv
