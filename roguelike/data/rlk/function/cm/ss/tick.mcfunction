# 작은 번개 슬라임 (@s, at @s): 빠르게 뛰어 와 1.7칸 안에서 달라붙음 → 바닥 고리(반경 1.5) 1초 → 작은 감전(6, 번개)
execute if score @s cmS matches 1 run return run function rlk:cm/ss/latch
scoreboard players remove @s c2T 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s c2T 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..1.7] if data entity @s {OnGround:1b} run return run function rlk:cm/ss/start
execute if score #free tmp matches 1 if score @s c2T matches ..0 run function rlk:cm/ss/hop
