# Stand-in intro tick (#sq kn 1..150).
execute if score #sq kn matches 34 run function rlk:boss/arlecchino/rig_stub/look/props/none
execute if score #sq kn matches 60 run function rlk:boss/arlecchino/rig_stub/look/weapon_r/hand
execute if score #sq kn matches 80 run function rlk:mboss/title {title:"「아를레키노」",sub:"우인단 집행관 서열 4위",color:"#E0303A"}
execute if score #sq kn matches 80 run function rlk:mboss/line/say {t:"두려운가? 아니면 두려워할 용기조차 없는 건가?",c:"#FF9AA8",gap:2,hold:50,snd:1}
execute if score #sq kn matches 140 at @s run function rlk:mboss/push/ring {r:40,to:45,kb:4}
execute if score #sq kn matches 150.. run scoreboard players set #sqdone kn 1
