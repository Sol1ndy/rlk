# {set} (anywhere): the proxy state set of the running proxy boss (a key of its manifest states). Literal lines per
# boss and set (no $(..) function names); an unknown set name changes nothing and warns.
$data modify storage rlk:mboss pxq set value "$(set)"
execute if score #mbPx mb matches 1 run tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"알 수 없는 판정 상태: ",color:"gray",bold:false},{nbt:"pxq",storage:"rlk:mboss",color:"gray"}]
