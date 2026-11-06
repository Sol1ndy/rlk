scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp /= #4 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
function rlk:mboss/line/say {t:"오아시스의 심장이 생명을 나눕니다",c:"#B6E35A",gap:2,hold:50,snd:1}
