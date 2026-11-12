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
# 가진 아이템의 효과 · 이름의 별을 바로 다시 계산(인벤 정리 · 장비 스캔). ench/pick 은 스스로도 표시하고, 홍련 보상(boss/scarlet/ev/item)은
# 인벤이 가득 차 지급이 미뤄질 때 이것뿐이다(예전에는 전투 중 핫바 아이템이 고쳐질 때의 정리가 대신 해 주었다)
scoreboard players set @a[tag=player] invDirty 2
