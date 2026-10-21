scoreboard players set #apTo mb 1
scoreboard players set #apToT mb 600
title @a[tag=player] title {text:"!",color:"#EDCF63"}
title @a[tag=player] subtitle {text:"오아시스의 심장이 위험합니다",color:"#C36E5A"}
function rlk:mboss/line/say {t:"파괴의 증식 생명체가 나타납니다",c:"#C36E5A",gap:2,hold:60,snd:2}
playsound minecraft:event.raid.horn hostile @a[tag=player] ~ ~ ~ 0.3 1 0.1
scoreboard players set #apHudQ mb 1
