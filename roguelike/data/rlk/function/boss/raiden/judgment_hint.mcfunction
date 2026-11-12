# The real game's prompt for 만겁 (instant kill), R2 allow-list.
title @a[tag=player] times 4 85 16
title @a[tag=player] subtitle {text:"「추모의 꽃다발」에 번개 원소 공격을 가해 보호막을 펼치세요",color:"aqua",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 105
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
