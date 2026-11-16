# 3틱마다 내 자리(몸에서 4칸, 무리 각도)로 끌림
scoreboard players set @s c2T 3
function rlk:cm/c3/turn
scoreboard players set #c2Fw tmp 210
scoreboard players set #c2Up tmp -1
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^4 unless entity @s[distance=..0.7] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
