# 번개가 닿음: 불(과부하) > 빙결·얼음(초전도) > 물(감전) > 활성(촉진) > 풀(활성) > 부착
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:3}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/overload {e:"Fire"}
execute if score @s frzT matches 1.. run return run function rlk:element/rx/supercond_frozen
execute if score @s aIce matches 1.. run return run function rlk:element/rx/supercond {e:"Ice"}
execute if score @s aWater matches 1.. run return run function rlk:element/rx/ec {e:"Thunder"}
execute if score @s quickT matches 1.. run return run function rlk:element/rx/additive {m:115,rx:15}
execute if score @s aGrass matches 1.. run return run function rlk:element/rx/quicken {e:"Grass"}
function rlk:element/attach {e:"Thunder"}
