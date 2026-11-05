# macro: id → 그 아이템의 강화 단계 +1 (최대 3). rlk:pinv enh.<id> 와 점수 <id> enhL (효과 배율 계산용)
scoreboard players set #enh tmp 0
$execute if data storage rlk:pinv enh.$(id) store result score #enh tmp run data get storage rlk:pinv enh.$(id)
scoreboard players add #enh tmp 1
# 화무십일홍이 ★★★ 가 되는 순간(2 → 3)만: 홍련의 한마디(나무위키 대사 그대로)
$data modify storage rlk:tmp eid set value "$(id)"
execute if score #enh tmp matches 3 if data storage rlk:tmp {eid:"sword_hwamu"} run tellraw @a[tag=player] {text:"",extra:[{text:"[홍련] ",color:"#E8466A"},{text:"화무십일홍이 한층 더 날카롭게 벼려졌네. 자, 이걸 이제 누구한테 휘두를지 지켜보게나.",color:"#F2D0E8"}]}
execute if score #enh tmp matches 4.. run scoreboard players set #enh tmp 3
$execute store result storage rlk:pinv enh.$(id) int 1 run scoreboard players get #enh tmp
$scoreboard players operation $(id) enhL = #enh tmp
# 효과 상수 · 설명 숫자 다시 계산
$execute if data storage rlk:tune t.$(id) run function rlk:items/tune/apply {id:"$(id)"}
