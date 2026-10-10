summon minecraft:armor_stand ~ ~ ~ {Tags:["rlk_view","rlk_vseat","rlk_pet"],Small:1b,Invisible:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,NoBasePlate:1b,DisabledSlots:4144959}
ride @e[tag=rlk_vseat,limit=1] mount @e[tag=rlk_av,limit=1]
function rlk:view/ride_apply
tellraw @s [{"text":"[시점] ","color":"gold","bold":true},{"text":"F5 위쪽 시점입니다. ","color":"#7FD3FF","bold":false},{"keybind":"key.togglePerspective","color":"yellow","bold":true},{"text":" 키를 눌러 3인칭(뒤에서 보기)으로 바꿔 주세요.","color":"gray","bold":false}]
