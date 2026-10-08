# 이번 테마의 장식 목록을 rlk:room q 로 (macro: l = a 바닥·벽 무늬 / b 프롭)
$execute if score #th room matches 1 run data modify storage rlk:room q set from storage rlk:room zb.$(l)1
$execute if score #th room matches 2 run data modify storage rlk:room q set from storage rlk:room zb.$(l)2
