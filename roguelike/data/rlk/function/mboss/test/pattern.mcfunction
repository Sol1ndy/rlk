# Module test hook (rlk:mboss/<id>/test {id:N}); the meaning of N belongs to the module. {id:"help"}: test/help_pattern.
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_pattern
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 중간보스가 없습니다.",color:"gray",bold:false}]
$function rlk:mboss/d/test {id:$(id)}
$tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"다음 패턴 요청: $(id)",color:"gray",bold:false}]
