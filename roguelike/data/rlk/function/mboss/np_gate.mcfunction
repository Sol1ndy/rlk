# The gate of the unparriable-attack warning (np_glint / np_glint_here): #npOk mb 1 = draw it now. Once per #npGap tmp
# ticks (a volley warns once); never while a cutscene runs; a module that draws its own warnings sets #mbNpOwn mb 1.
scoreboard players set #npOk mb 0
execute if score #mbNpOwn mb matches 1 run return 0
execute if score #mbCine mb matches 1 run return 0
execute store result score #npNow mb run time query gametime
# VP beat: on the beat's clock
scoreboard players operation #npNow mb -= #btAdj cb
scoreboard players operation #t mb = #npNow mb
scoreboard players operation #t mb -= #mbNpAt mb
execute if score #t mb < #npGap tmp run return 0
scoreboard players operation #mbNpAt mb = #npNow mb
scoreboard players set #npOk mb 1
