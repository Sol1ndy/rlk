# Stand-in intro tick (#sq hr 1..640).
execute if score #sq hr matches 248 run function rlk:mboss/mv/face
execute if score #sq hr matches 300 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 312 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 324 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 336 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 348 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 360 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 372 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 384 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 396 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 408 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 420 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 432 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 444 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 456 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 468 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 480 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 492 run function rlk:boss/scarlet/core/sq/intro/walk
execute if score #sq hr matches 554 run function rlk:boss/scarlet/rig_stub/play/intro_end
execute if score #sq hr matches 610 run function rlk:mboss/title {title:"홍련",sub:"월하곡",color:"#E8466A"}
execute if score #sq hr matches 630 run function rlk:boss/scarlet/core/sq/intro/k/630
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
