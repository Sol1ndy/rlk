# An empty (or short) buffer: six copies of this sample.
data modify storage rlk:mboss lv set value [{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0},{x:0,z:0}]
execute store result storage rlk:mboss lv[0].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[0].z int 1 run scoreboard players get #lz mb
execute store result storage rlk:mboss lv[1].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[1].z int 1 run scoreboard players get #lz mb
execute store result storage rlk:mboss lv[2].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[2].z int 1 run scoreboard players get #lz mb
execute store result storage rlk:mboss lv[3].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[3].z int 1 run scoreboard players get #lz mb
execute store result storage rlk:mboss lv[4].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[4].z int 1 run scoreboard players get #lz mb
execute store result storage rlk:mboss lv[5].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[5].z int 1 run scoreboard players get #lz mb
