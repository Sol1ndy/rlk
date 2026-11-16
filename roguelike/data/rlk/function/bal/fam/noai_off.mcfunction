# a freeze still on keeps NoAI and restores the mob's own state when it ends (element/frz_end); else restore it here
execute if score @s frzT matches 1.. run return run function rlk:bal/fam/noai_pass
execute unless entity @s[tag=rlk_bal_noai] run data merge entity @s {NoAI:0b}
tag @s remove rlk_bal_noai
