# The blast: the Heart -1400 (no progress for it), the green dome + sounds; it is spent (no pay) and tumbles away.
function rlk:boss/apep/heart/sub {v:1400}
execute at @s run function rlk:boss/apep/fx/snd/o7_blast
execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/p/blast_dome
tag @s add rlk_mb_ap_spent
tag @s add rlk_mb_ap_dying
tag @s add rlk_mb_inv
scoreboard players set @s apT 0
function rlk:boss/apep/om/destr/play/org_die
