# 교활한 통수 (whip, id 7) - tick
scoreboard players set #azPLen mb 64
execute if score #azPT mb matches 2..25 run return run function rlk:boss/azhdaha/p/whip/kd/2_25
execute if score #azPT mb matches 26..64 run return run function rlk:boss/azhdaha/p/whip/kd/26_64
