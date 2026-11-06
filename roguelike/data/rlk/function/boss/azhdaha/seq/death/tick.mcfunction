# Death beats on #mbT (clip tick = #mbT - 1); the seal and the petrify at "still"; the scale-out
# 120 -> 140.
execute if score #mbT mb matches 35 run function rlk:boss/azhdaha/seq/death/chin
execute if score #mbT mb matches 67 run function rlk:boss/azhdaha/seq/death/tail
execute if score #mbT mb matches 81 run function rlk:mboss/line/say {t:"모…락스…!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #mbT mb matches 93 run function rlk:boss/azhdaha/seq/death/head
execute if score #mbT mb matches 97 run function rlk:boss/azhdaha/seq/death/seal
execute if score #mbT mb matches 101 run function rlk:boss/azhdaha/fx/p/petrify_pulse
execute if score #mbT mb matches 121 run function rlk:boss/azhdaha/seq/death/out
