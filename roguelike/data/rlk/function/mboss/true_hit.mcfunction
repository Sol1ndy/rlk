# True damage to @s (any rlk_mob, normally the body) at @s: #mbTrue mb = damage, #mbTrueEl mb = colour
# of the number (#elem). Goes through combat/apply (kill, rewards, death_start) but skips elements,
# modifiers, RES and the module hooks (#trueDmg). Never call it from inside combat/apply.
scoreboard players add #hitLanded tmp 0
scoreboard players operation #mbSaveHL mb = #hitLanded tmp
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = #mbTrue mb
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #basic itv 0
scoreboard players set #bowHit tmp 0
scoreboard players operation #elem tmp = #mbTrueEl mb
scoreboard players set #tfm tmp 1
scoreboard players set #trueDmg tmp 1
function rlk:combat/apply
scoreboard players set #trueDmg tmp 0
scoreboard players set #tfm tmp 0
scoreboard players operation #hitLanded tmp = #mbSaveHL mb
