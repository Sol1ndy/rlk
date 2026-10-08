# 원소폭발 아이템의 반짝임: 섬광 중(진 사용 가능) 또는 뱀의 계략 50pt 이상(멸 사용 가능)
data modify storage rlk:chars it.glint set value "false"
execute if score #bs tmp matches 0 if score @s skM matches 1.. run data modify storage rlk:chars it.glint set value "true"
execute if score #bs tmp matches 0 unless score @s skM matches 1.. if score @s energy >= #skBurstMin tmp run data modify storage rlk:chars it.glint set value "true"
