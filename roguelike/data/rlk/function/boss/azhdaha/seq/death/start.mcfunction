# The death (plan 5 D), clip tick 0: the first line, the sting (the framework stopped the music).
function rlk:mboss/line/say {t:"난… 사라지지 않아!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:boss/azhdaha/fx/snd/death_sting
playsound minecraft:entity.ravager.hurt hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
