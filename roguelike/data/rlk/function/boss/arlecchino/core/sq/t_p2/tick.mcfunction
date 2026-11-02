# Stand-in t_p2 tick (#sq kn 1..180).
execute if score #sq kn matches 0 run function rlk:boss/arlecchino/rig_stub/look/glow/crimson
execute if score #sq kn matches 50 run effect give @a[tag=player] minecraft:blindness 1 0 true
execute if score #sq kn matches 90 run function rlk:boss/arlecchino/rig_stub/look/form/p2
execute if score #sq kn matches 90 run function rlk:boss/arlecchino/rig_stub/look/weapon_l/hand
execute if score #sq kn matches 140 run function rlk:mboss/title {title:"두 세계 불의 잔재",sub:"페르엘",color:"#C8102E"}
execute if score #sq kn matches 140 run function rlk:mboss/line/say {t:"보아라, 모든 선의를 불태울 칼날을!",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #sq kn matches 140 run function rlk:boss/arlecchino/rig_stub/look/glow/normal
execute if score #sq kn matches 180.. run scoreboard players set #sqdone kn 1
