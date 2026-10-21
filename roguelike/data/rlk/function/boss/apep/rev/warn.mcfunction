# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The time-out warning (neutral information; plan 7.6.3): the "!" title, the line, the horn.
scoreboard players set #apTo mb 1
scoreboard players set #apToT mb 600
function rlk:boss/apep/fx/hud/title {g:"warn",t:"오아시스의 심장이 위험합니다",c:"#C36E5A",s:"",hold:50}
function rlk:mboss/line/say {t:"파괴의 증식 생명체가 나타납니다",c:"#C36E5A",gap:2,hold:60,snd:2}
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/timeout_warn
scoreboard players set #apHudQ mb 1
