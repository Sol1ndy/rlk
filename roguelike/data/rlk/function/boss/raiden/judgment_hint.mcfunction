title @a[tag=player] times 4 85 16
title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 105
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
