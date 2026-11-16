# 1~2번째 맵: 졸개 무리 + 번개 슬라임 (방이 클수록 무리가 커짐)
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 5.. run scoreboard players add #c2n tmp 1
execute if score #c2N tmp matches 7.. run scoreboard players add #c2n tmp 1
function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 6.. run scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sl"}
