# The chapter boss was killed (@s = zone marker): title, the test replay links, forget. Returns 1.
title @a[tag=player] times 8 50 14
title @a[tag=player] subtitle {text:"다음 챕터로 가는 길이 열렸습니다",color:"#FFE08A"}
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
return 1
