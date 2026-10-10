# Cannon remains planted at its validated 3x3 site, including when the target is far away.
function rlk:cm/cn/stabilize
execute if score @s cmS matches 1 run return run function rlk:cm/cn/fuse
execute if score @s cmS matches 2 run return run function rlk:cm/cn/wait
execute if score @s cmCd matches ..0 unless score @s frzT matches 1.. if entity @e[tag=rlk_body,distance=..24] run function rlk:cm/cn/start
