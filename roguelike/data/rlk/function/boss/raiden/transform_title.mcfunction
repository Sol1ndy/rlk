# After her line: the form name and the armour hint.
title @a[tag=player] times 8 55 16
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
title @a[tag=player] title {text:"악요의 요고우 텐마",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 79
scoreboard players set @a[tag=player] ttlT 79
scoreboard players set #rdCap rd 1
# Not a pattern caption: an interrupted illusion caption must not let armor_start's
# finish (rdTime 56) cut this one short.
scoreboard players set #rdCapPat rd 0
