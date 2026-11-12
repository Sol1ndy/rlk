# @s = body: the balance clock is over: her stun ends now if it still runs (recovery, the AI).
execute if score #pat kn matches 50 if score #stun kn matches 1 run function rlk:boss/arlecchino/core/stun_end
