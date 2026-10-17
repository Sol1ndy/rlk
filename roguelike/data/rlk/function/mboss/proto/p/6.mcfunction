# Pattern 6 "끌어당겨 회전베기" (@s = body, at @s; #prT = 1.. pattern clock).
execute if score #prT mb matches 1 run function rlk:mboss/proto/pose/both_up {d:12}
execute if score #prT mb matches 1 run function rlk:mboss/line/say {t:"이리 오너라.",c:"#E8C890",gap:2,hold:26,snd:2}
execute if score #prT mb matches 1..27 run function rlk:mboss/proto/pull_tell
execute if score #prT mb matches 28 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.6 positioned ~ 201 ~ run function rlk:mboss/pull/start {t:6}
execute if score #prT mb matches 28 run playsound minecraft:entity.evoker.prepare_wololo hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.3
execute if score #prT mb matches 36 run function rlk:mboss/proto/pose/sweep_wind {d:5}
execute if score #prT mb matches 36 run scoreboard players set #hzSfx mb 2
execute if score #prT mb matches 36 run execute positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:55,a:180,tell:14,dmg:120}
execute if score #prT mb matches 49 run function rlk:mboss/proto/pose/sweep {d:3}
execute if score #prT mb matches 66 run function rlk:mboss/proto/finish
