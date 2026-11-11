# After a move (@s = the body): standing in the player's camera line (the player moved since her stop was chosen) she
# steps 1.8 b out of it in 2 t - to her right, her left or back - wherever mv/ok and core/cam_ok pass.
execute at @s positioned ~ 201 ~ if function rlk:boss/scarlet/core/cam_ok run return 0
execute at @s positioned ~ 201 ~ rotated as @s rotated ~-90 0 positioned ^ ^ ^1.8 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:mboss/mv/glide {t:2}
execute at @s positioned ~ 201 ~ rotated as @s rotated ~90 0 positioned ^ ^ ^1.8 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:mboss/mv/glide {t:2}
execute at @s positioned ~ 201 ~ rotated as @s rotated ~180 0 positioned ^ ^ ^1.8 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:mboss/mv/glide {t:2}
