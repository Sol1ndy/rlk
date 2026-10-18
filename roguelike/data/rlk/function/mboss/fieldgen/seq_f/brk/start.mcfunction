# S3 break 0 (@s = body; brk/begin after the 20th count: the hazards, decals, banner and meter are gone): the
# cracked bubble lights up white-gold (at the grounded core for break_low: FID-1).
execute unless score #fgBrkLo mb matches 1 positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/p/bubble_glow
execute if score #fgBrkLo mb matches 1 positioned ~ ~1.3 ~ run function rlk:mboss/fieldgen/fx/p/bubble_glow
function rlk:mboss/fieldgen/fx/snd/break_glow
