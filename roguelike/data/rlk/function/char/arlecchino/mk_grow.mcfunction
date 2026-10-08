# 방금 생긴 표식 조각을 제 크기로 (0.25초 동안 가운데에서 커짐). 조각마다 자기 몹의 가운데(armY · armZ) 기준
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p0] run function rlk:char/arlecchino/mk_grow_0
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p1] run function rlk:char/arlecchino/mk_grow_1
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p2] run function rlk:char/arlecchino/mk_grow_2
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p3] run function rlk:char/arlecchino/mk_grow_3
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p4] run function rlk:char/arlecchino/mk_grow_4
execute as @e[tag=rlk_armk_new,tag=rlk_armk_p5] run function rlk:char/arlecchino/mk_grow_5
tag @e[tag=rlk_armk_new] remove rlk_armk_new
