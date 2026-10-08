# 얼음이 닿음: 불(융해 ×1.5) > 번개(초전도) > 물(빙결) > 부착 (풀·활성과는 공존)
execute if score @s aVoid matches 1.. run return run function rlk:element/rx/void {e:"Void",n:4}
execute if score @s aFire matches 1.. run return run function rlk:element/rx/amp {e:"Fire",use:50,mul:150,rx:2}
execute if score @s aThunder matches 1.. run return run function rlk:element/rx/supercond {e:"Thunder"}
execute if score @s aWater matches 1.. run return run function rlk:element/rx/freeze {e:"Water"}
function rlk:element/attach {e:"Ice"}
