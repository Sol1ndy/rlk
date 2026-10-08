# 풀이 닿음: 불(연소) > 물(개화) > 활성(발산) > 번개(활성) > 부착 (얼음과는 공존)
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:7}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/burn_grass
execute if score @s aWater matches 1.. run return run function rlk:element/rx/bloom {e:"Water",use:200}
execute if score @s quickT matches 1.. run return run function rlk:element/rx/additive {m:125,rx:16}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/quicken {e:"Thunder"}
function rlk:element/attach {e:"Grass"}
