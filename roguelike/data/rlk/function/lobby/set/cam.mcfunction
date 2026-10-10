# 카메라 위치 = 거리(뒤) · 좌우 · 높이 (rlk:lobby cfg)
execute if data storage rlk:lobby cfg{dist:0} run data modify storage rlk:view cam.back set value 2.6d
execute if data storage rlk:lobby cfg{dist:1} run data modify storage rlk:view cam.back set value 3.3d
execute if data storage rlk:lobby cfg{dist:2} run data modify storage rlk:view cam.back set value 4.3d
execute if data storage rlk:lobby cfg{side:0} run data modify storage rlk:view cam.right set value 0.9d
execute if data storage rlk:lobby cfg{side:1} run data modify storage rlk:view cam.right set value -0.9d
execute if data storage rlk:lobby cfg{h:0} run data modify storage rlk:view cam.up set value 0.0d
execute if data storage rlk:lobby cfg{h:1} run data modify storage rlk:view cam.up set value 0.3d
execute if data storage rlk:lobby cfg{h:2} run data modify storage rlk:view cam.up set value 0.65d
function rlk:view/cam_calc
# F5 위쪽 시점: 거리 2.5 / 3.5 / 4.5 · 받침(머리 위 높이) 0.25 / 0.5 / 1
execute if data storage rlk:lobby cfg{dist:0} run data modify storage rlk:view ride.d set value 2.5d
execute if data storage rlk:lobby cfg{dist:1} run data modify storage rlk:view ride.d set value 3.5d
execute if data storage rlk:lobby cfg{dist:2} run data modify storage rlk:view ride.d set value 4.5d
execute if data storage rlk:lobby cfg{h:0} run data modify storage rlk:view ride.s set value 0.25d
execute if data storage rlk:lobby cfg{h:1} run data modify storage rlk:view ride.s set value 0.5d
execute if data storage rlk:lobby cfg{h:2} run data modify storage rlk:view ride.s set value 1.0d
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_apply
