# 불이 닿음: 얼음/빙결(융해 ×2) > 물(증발 ×1.5) > 번개(과부하) > 풀·활성(연소) > 부착
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:1}
execute if score @s frzT matches 1.. run return run function rlk:element/rx/melt_frozen
execute if score @s aIce matches 1.. run return run function rlk:element/rx/amp {e:"Ice",use:200,mul:200,rx:2}
execute if score @s aWater matches 1.. run return run function rlk:element/rx/amp {e:"Water",use:50,mul:150,rx:1}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/overload {e:"Thunder"}
execute if score @s quickT matches 1.. run function rlk:element/quick_to_grass
function rlk:element/attach {e:"Fire"}
execute if score @s aGrass matches 1.. run function rlk:element/rx/burn
