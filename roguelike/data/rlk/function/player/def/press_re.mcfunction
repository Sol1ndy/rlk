# @s = 플레이어. 받지 않는 동안 또 누른 F: 받지 않는 시간을 지금 + #parRe 까지로 늘린다(늦출 뿐 당기지 않음)
scoreboard players operation #t cb = #now cb
scoreboard players operation #t cb += #parRe tmp
scoreboard players operation @s parLk > #t cb
