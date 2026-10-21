# One typing step of a boss line (macro: t text, c colour, s stay, f fade, n ttlT, e 1 = the last step).
# One plain, quiet tick per step (same sound and pitch every time).
$title @a[tag=player] times 0 $(s) $(f)
$title @a[tag=player] subtitle {text:"$(t)",color:"$(c)",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
$scoreboard players set @a[tag=player] ttlT $(n)
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ .3 1 0
$scoreboard players set #rdSgLineEnd rd $(e)
execute if score #rdSgLineEnd rd matches 1 run scoreboard players set #rdLine rd 0
