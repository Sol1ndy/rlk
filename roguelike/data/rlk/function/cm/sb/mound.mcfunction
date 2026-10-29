# 모래 둔덕(예고 0.8초): 둔덕이 부풀며 떨림 · 모래가 튐. 아직 맞힐 수 없음
execute if score @s c2T matches 1.. if score @s c2T matches 2..15 run particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.25 0.1 0.25 0 1 normal
execute if score @s c2T matches 1..6 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.15 ~ 0.25 0.05 0.25 0.05 3 normal
execute if score @s c2T matches ..0 run function rlk:cm/sb/erupt
