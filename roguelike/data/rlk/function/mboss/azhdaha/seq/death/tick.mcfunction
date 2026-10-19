# Death beats on #mbT (clip tick = #mbT - 1); the scale-out 120 -> 140.
execute if score #mbT mb matches 35 run playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
execute if score #mbT mb matches 67 run playsound minecraft:entity.ravager.death hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute if score #mbT mb matches 81 run function rlk:mboss/line/say {t:"모…락스…!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #mbT mb matches 93 run function rlk:mboss/azhdaha/kstub/snd/death_fall
execute if score #mbT mb matches 97 run function rlk:mboss/azhdaha/seq/death/seal
execute if score #mbT mb matches 121 run function rlk:mboss/azhdaha/seq/death/out
