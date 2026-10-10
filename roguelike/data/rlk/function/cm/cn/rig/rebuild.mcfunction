# Existing mannequin and old block cannon are replaced only for this cmId.
function rlk:cm/cn/rig/select
kill @e[tag=rlk_cn_this]
execute as @e[tag=rlk_cmv] if score @s cmId = #cnId tmp run kill @s
execute as @e[tag=rlk_cmcan] if score @s cmId = #cnId tmp run kill @s
scoreboard players set @s cmAF 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
function rlk:cm/cn/stabilize
function rlk:cm/cn/rig/create
