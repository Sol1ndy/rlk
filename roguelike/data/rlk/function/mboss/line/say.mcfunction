# Typed subtitle: {t:"text",c:"#colour",gap:ticks per step,hold:ticks the full line stays,snd:0 none/1 soft/2 stern}.
# Grows two characters per step with a quiet tick; a new line replaces the running one.
$data modify storage rlk:mboss ln set value {t:"$(t)",c:"$(c)",n:0,stay:0}
$scoreboard players set #mbLnGap mb $(gap)
$scoreboard players set #mbLnHold mb $(hold)
$scoreboard players set #mbLnSnd mb $(snd)
execute if score #mbLnGap mb matches ..0 run scoreboard players set #mbLnGap mb 1
execute store result score #mbLnLen mb run data get storage rlk:mboss ln.t
scoreboard players set #mbLnN mb 0
scoreboard players set #mbLnT mb 0
scoreboard players set #mbLn mb 1
execute if score #mbLnSnd mb matches 1 as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.resonate voice @s ~ ~ ~ 0.6 0.8
execute if score #mbLnSnd mb matches 2 as @a[tag=player] at @s run playsound minecraft:block.bell.resonate voice @s ~ ~ ~ 0.45 0.55
function rlk:mboss/line/step
