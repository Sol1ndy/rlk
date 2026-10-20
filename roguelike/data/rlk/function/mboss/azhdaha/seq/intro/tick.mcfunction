# Intro beats on #mbT (clip tick = #mbT - 1; untargetable until the core ends the intro at the clip end).
execute if score #mbT mb matches 1 run function rlk:mboss/azhdaha/fx/snd/intro_drone
execute if score #mbT mb matches 26 run function rlk:mboss/azhdaha/fx/snd/intro_thump
execute if score #mbT mb matches 31 run function rlk:mboss/azhdaha/fx/snd/intro_thump
execute if score #mbT mb matches 51 run function rlk:mboss/azhdaha/seq/intro/shatter_0
execute if score #mbT mb matches 71 run function rlk:mboss/azhdaha/seq/intro/shatter_3
execute if score #mbT mb matches 113 run function rlk:mboss/azhdaha/seq/intro/seal
execute if score #mbT mb matches 117 run function rlk:mboss/azhdaha/fx/snd/intro_thump
execute if score #mbT mb matches 121 run function rlk:mboss/azhdaha/seq/intro/roar
execute if score #mbT mb matches 131 run function rlk:mboss/azhdaha/seq/intro/blast
