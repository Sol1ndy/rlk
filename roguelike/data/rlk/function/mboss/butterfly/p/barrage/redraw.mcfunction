# @s = a landing marker: it lands when #bfPT reaches its mbT; the module tick after this hook counts #bfPT
# up once more, so the landing is mbT - #bfPT - 1 ticks from now.
scoreboard players operation #bp12W mb = @s mbT
scoreboard players operation #bp12W mb -= #bfPT mb
scoreboard players remove #bp12W mb 1
execute if score #bp12W mb matches 1.. run function rlk:mboss/butterfly/p/barrage/tele/pick
