# 카메라(F5 위쪽 시점) = 거리 · 높이 (rlk:lobby cfg): 거리 2.5 / 3.5 / 4.5칸 · 받침(머리 위 높이) 0.25 / 0.5 / 1칸
execute if data storage rlk:lobby cfg{dist:0} run data modify storage rlk:view ride.d set value 2.5d
execute if data storage rlk:lobby cfg{dist:1} run data modify storage rlk:view ride.d set value 3.5d
execute if data storage rlk:lobby cfg{dist:2} run data modify storage rlk:view ride.d set value 4.5d
execute if data storage rlk:lobby cfg{h:0} run data modify storage rlk:view ride.s set value 0.25d
execute if data storage rlk:lobby cfg{h:1} run data modify storage rlk:view ride.s set value 0.5d
execute if data storage rlk:lobby cfg{h:2} run data modify storage rlk:view ride.s set value 1.0d
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_apply
