function rlk:cm/cn/rig/select
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_cn_this] run tp @s ~ ~ ~ ~ 0
tag @e[tag=rlk_cn_this] remove rlk_cn_this
