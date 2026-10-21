# {set} (anywhere): the proxy state set of the running proxy boss (a key of its manifest states). Literal lines per
# boss and set (no $(..) function names); an unknown set name changes nothing and warns.
$data modify storage rlk:mboss pxq set value "$(set)"
execute if score #mbId mb matches 98 if data storage rlk:mboss {pxq:"normal"} run return run function rlk:mboss/px/cproto/s/normal
execute if score #mbId mb matches 98 if data storage rlk:mboss {pxq:"tail_only"} run return run function rlk:mboss/px/cproto/s/tail_only
execute if score #mbId mb matches 98 if data storage rlk:mboss {pxq:"inv"} run return run function rlk:mboss/px/cproto/s/inv
execute if score #mbId mb matches 98 if data storage rlk:mboss {pxq:"dead"} run return run function rlk:mboss/px/cproto/s/dead
execute if score #mbId mb matches 10 if data storage rlk:mboss {pxq:"normal"} run return run function rlk:mboss/px/azhdaha/s/normal
execute if score #mbId mb matches 10 if data storage rlk:mboss {pxq:"jump"} run return run function rlk:mboss/px/azhdaha/s/jump
execute if score #mbId mb matches 10 if data storage rlk:mboss {pxq:"inv"} run return run function rlk:mboss/px/azhdaha/s/inv
execute if score #mbId mb matches 10 if data storage rlk:mboss {pxq:"tail_only"} run return run function rlk:mboss/px/azhdaha/s/tail_only
execute if score #mbId mb matches 10 if data storage rlk:mboss {pxq:"dead"} run return run function rlk:mboss/px/azhdaha/s/dead
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"p1"} run return run function rlk:mboss/px/apep/s/p1
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"p3u"} run return run function rlk:mboss/px/apep/s/p3u
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"p3c"} run return run function rlk:mboss/px/apep/s/p3c
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"burrowed"} run return run function rlk:mboss/px/apep/s/burrowed
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"aloft"} run return run function rlk:mboss/px/apep/s/aloft
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"inv"} run return run function rlk:mboss/px/apep/s/inv
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"parked"} run return run function rlk:mboss/px/apep/s/parked
execute if score #mbId mb matches 11 if data storage rlk:mboss {pxq:"dead"} run return run function rlk:mboss/px/apep/s/dead
execute if score #mbPx mb matches 1 run tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"알 수 없는 판정 상태: ",color:"gray",bold:false},{nbt:"pxq",storage:"rlk:mboss",color:"gray"}]
