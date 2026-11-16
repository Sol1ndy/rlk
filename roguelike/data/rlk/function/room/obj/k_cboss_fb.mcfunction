# (매크로 = rlk:mboss cbyid.<id>, 레지스트리 기록) 문 표시 저장소 없이 문을 세움: 아이콘 하나 + 이름 + 설명(room/obj/make_node), 회색 경고
$tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"문 표시 정보가 없어 기본 문을 세웠습니다($(id)).",color:"gray",bold:false}]
scoreboard players set #oact tmp 16
$scoreboard players set #oarg tmp $(n)
$function rlk:room/obj/make_node with storage rlk:mboss cbyid.$(id).gate
