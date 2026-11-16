# Untargetable intro (rlk_mb_inv). The module ends it with mboss/intro_end; cur.intro is the maximum.
function rlk:mboss/d/intro_tick
execute if score #mbSt mb matches 0 if score #mbT mb >= #mbIntro mb run function rlk:mboss/intro_end
