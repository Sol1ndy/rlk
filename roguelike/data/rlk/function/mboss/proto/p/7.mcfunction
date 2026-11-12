# Pattern 7 "전역 강타" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/both_up {d:12}
execute if score #prT mb matches 1 run function rlk:mboss/line/say {t:"피할 곳은 한 곳뿐.",c:"#E8C890",gap:2,hold:30,snd:2}
execute if score #prT mb matches 1 run function rlk:mboss/proto/safe_spot
execute if score #prT mb matches 44 run function rlk:mboss/proto/pose/both_down {d:3}
execute if score #prT mb matches 46 run kill @e[tag=rlk_mb_proto_safe]
execute if score #prT mb matches 60 run function rlk:mboss/proto/finish
