# A hazard-bound display sits exactly on its hazard origin; one without a hazard there is an orphan.
tag @e[tag=rlk_rd_hvis] add rlk_rd_orph
execute as @e[tag=rlk_rd_hazard] at @s run tag @e[tag=rlk_rd_orph,distance=..0.05] remove rlk_rd_orph
kill @e[tag=rlk_rd_orph]
