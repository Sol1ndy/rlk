# From rlk:tick while #mbLowG mb is not 1 and something still carries low gravity (any player or avatar tagged
# rlk_lowg: a field that ended, broke or paused, a fight that is over, a relog or crash mid-field, a view switch).
execute as @e[tag=rlk_lowg] run function rlk:mboss/lowg_rem
