# 카메라(플레이어의 눈)를 이 자리에 (@s = 플레이어). 받침(item_display)에 태워서 부드럽게 따라가게 한다: 눈 = 받침 + 1.02
tp @e[tag=rlk_camv,limit=1] ~ ~-1.02 ~
# 웅크리면 탈것에서 내려지므로, 웅크린 동안은 직접 옮긴다(눈높이 1.27)
execute if predicate rlk:in_sneak run return run tp @s ~ ~-1.27 ~
ride @s mount @e[tag=rlk_camv,limit=1]
