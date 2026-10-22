# 잠긴 칸(inventory.(9+invCap)~26)을 방벽으로 채움. 이미 방벽이면 그대로 (@s = 플레이어, #si = 첫 잠긴 칸)
execute if score #si tmp matches ..26 run function rlk:player/inv/place_lock_one
