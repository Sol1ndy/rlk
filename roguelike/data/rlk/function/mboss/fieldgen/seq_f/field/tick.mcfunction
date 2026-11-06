# The field ambience (@s = body, every module tick while #fgField >= 1; frozen with the fight): pebbles at the
# player's feet every 20 t while low gravity holds (never at the eyes; not during the waves: their fire bands,
# three at once with the triple front, need the kit's card room, and a pebble card lives up to 66 t), the violet crackle under the core every
# 20 t in the field form (not during the waves: their own fx), the field drone every 40 t, the settle's gold
# streaks 13 / 28 t after the opening (#fgCool from 40), the first field's low-gravity notice
# when the banner's hold ends (spec S5: what low gravity does).
scoreboard players operation #fgM mb = #fgClk mb
scoreboard players operation #fgM mb %= #fgK20 mb
execute if score #fgLowG mb matches 1 if score #fgM mb matches 0 unless score #fgPat mb matches 21 at @e[tag=rlk_body,limit=1] run function rlk:mboss/fieldgen/fx/p/pebbles
execute if score #fgField mb matches 2..4 if score #fgM mb matches 10 unless score #fgPat mb matches 21 positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/p/field_idle
scoreboard players operation #fgM mb = #fgClk mb
scoreboard players operation #fgM mb %= #fgK40 mb
execute if score #fgField mb matches 2..4 if score #fgM mb matches 20 run function rlk:mboss/fieldgen/fx/snd/field_hum
execute if score #fgField mb matches 2 if score #fgPat mb matches 0 if score #fgCool mb matches 28 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/gold_streaks
execute if score #fgField mb matches 2 if score #fgPat mb matches 0 if score #fgCool mb matches 13 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/gold_streaks
execute if score #fgFN mb matches 1 if score #fgFirstT mb matches 101 if score #fgLowG mb matches 1 run function rlk:mboss/fieldgen/fx/hud/ab_lowg
