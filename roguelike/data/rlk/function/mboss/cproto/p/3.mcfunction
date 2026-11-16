# 3: the mask hazard: hit everywhere except within 2.5 b of its two safe markers (the body and a spot 5 b south).
execute if score #cpT mb matches 1 run function rlk:mboss/cproto/mask
execute if score #cpT mb matches 50.. run scoreboard players set #cpPat mb 0
