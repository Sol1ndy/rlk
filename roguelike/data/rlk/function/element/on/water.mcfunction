# 물이 닿음: 불(증발 ×2) > 얼음(빙결) > 번개(감전) > 풀·활성(개화) > 부착
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:2}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/amp {e:"Fire",use:200,mul:200,rx:1}
execute if score @s aIce matches 1.. run return run function rlk:element/rx/freeze {e:"Ice"}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/ec {e:"Water"}
execute if score @s aGrass matches 1.. run return run function rlk:element/rx/bloom {e:"Grass",use:50}
execute if score @s quickT matches 1.. run return run function rlk:element/rx/bloom {e:"Grass",use:0}
function rlk:element/attach {e:"Water"}
