# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end).
function rlk:mboss/proto/rig/follow
execute if score #mbT mb matches 1 run function rlk:mboss/proto/pose/both_up {d:4}
execute if score #mbT mb matches 1 positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:24}
execute if score #mbT mb matches 1 run scoreboard players set #hzSfx mb 1
execute if score #mbT mb matches 1 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:24,dmg:100}
execute if score #mbT mb matches 21 run function rlk:mboss/proto/pose/both_down {d:3}
execute if score #mbT mb matches 25 run particle minecraft:explosion ~ ~0.5 ~ 0.8 0.1 0.8 0 3 force @a[tag=player]
execute if score #mbT mb matches 28 run function rlk:mboss/line/say {t:"시험을 시작하지.",c:"#E8C890",gap:2,hold:30,snd:1}
execute if score #mbT mb matches 32 run function rlk:mboss/proto/pose/rest {d:8}
execute if score #mbT mb matches 50.. run function rlk:mboss/intro_end
