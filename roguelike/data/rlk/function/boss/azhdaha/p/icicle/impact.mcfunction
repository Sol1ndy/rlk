# (FIX perf, STATE-14) the frost burst only while < 44 kit fx cards live (the 64 cap less two bursts): a
# 43 impact on the tick of another pattern's hit visuals (45 eruption, P1 impact, rings) sheds its
# flourish instead of cutting theirs; the shatter sounds always play.
execute unless score #akN mb matches 44.. run function rlk:boss/azhdaha/fx/p/frost_burst {r:16}
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
