# macro: c(상수 이름), x(곱), d(나눔), p(소수 자리 0~2), u(단위) → rlk:tune ftext
$scoreboard players operation #fv tmp = $(c) tmp
$scoreboard players set #fx tmp $(x)
$scoreboard players set #fd tmp $(d)
execute if score #fd tmp matches ..0 run scoreboard players set #fd tmp 1
$scoreboard players set #fp tmp $(p)
scoreboard players set #fs tmp 1
execute if score #fp tmp matches 1 run scoreboard players set #fs tmp 10
execute if score #fp tmp matches 2.. run scoreboard players set #fs tmp 100
# w = 반올림(v × x × 10^p ÷ d)
scoreboard players operation #fv tmp *= #fx tmp
scoreboard players operation #fv tmp *= #fs tmp
scoreboard players operation #fh tmp = #fd tmp
scoreboard players operation #fh tmp /= #2 tmp
scoreboard players operation #fv tmp += #fh tmp
scoreboard players operation #fv tmp /= #fd tmp
scoreboard players operation #fi tmp = #fv tmp
scoreboard players operation #fi tmp /= #fs tmp
scoreboard players operation #ff tmp = #fv tmp
scoreboard players operation #ff tmp %= #fs tmp
execute store result storage rlk:tune f.i int 1 run scoreboard players get #fi tmp
execute store result storage rlk:tune f.f int 1 run scoreboard players get #ff tmp
$data modify storage rlk:tune f.u set value "$(u)"
# 소수가 0 이면 정수만. 소수 둘째 자리: 끝자리가 0 이면 한 자리로(1.50 → 1.5), 한 자리 수면 앞에 0(1.05)
execute if score #ff tmp matches 0 run return run function rlk:items/tune/fmt0 with storage rlk:tune f
execute if score #fp tmp matches ..1 run return run function rlk:items/tune/fmt1 with storage rlk:tune f
scoreboard players operation #fr tmp = #ff tmp
scoreboard players operation #fr tmp %= #10 tmp
execute if score #fr tmp matches 0 run scoreboard players operation #ff tmp /= #10 tmp
execute if score #fr tmp matches 0 store result storage rlk:tune f.f int 1 run scoreboard players get #ff tmp
execute if score #fr tmp matches 0 run return run function rlk:items/tune/fmt1 with storage rlk:tune f
execute if score #ff tmp matches 1..9 run return run function rlk:items/tune/fmt2z with storage rlk:tune f
function rlk:items/tune/fmt1 with storage rlk:tune f
