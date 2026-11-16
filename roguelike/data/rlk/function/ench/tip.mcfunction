# 인챈트 화면에서 조준한 아이템의 설명 끝에 강화 안내 (macro: h = 보유 목록의 순번). tip/inv 다음에 실행
$execute unless data storage rlk:pinv order[$(h)] run return 0
$data modify storage rlk:lvpick b.id set from storage rlk:pinv order[$(h)]
scoreboard players set #enh tmp 0
function rlk:items/enh_get with storage rlk:lvpick b
data modify storage rlk:lvpick tip append value {text:"\n\n"}
execute if score #enh tmp matches 3.. run data modify storage rlk:lvpick tip append value {text:"최대로 강화되었습니다",color:"#FFD24A"}
execute if score #enh tmp matches ..2 run data modify storage rlk:lvpick tip append value {text:"클릭: 강화 (별 +1)",color:"#B58BE8"}
execute if score #enh tmp matches ..2 run data modify storage rlk:lvpick tip append value {text:"\n효과량이 늘고, 지속 시간이 길어지고, 재사용 대기가 짧아집니다",color:"gray"}
