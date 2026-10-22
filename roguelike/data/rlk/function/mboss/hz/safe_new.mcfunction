# A new mask safe group in #mbSafeG mb (cm.md 13.6, APEP-04): -1, -2, ... (back to -1 after -999 999), a number space of
# its own: hazard ids (mbHzI, also the default group of a mask made with #hzSafeG 0) are >= 1, so neither a mask of
# another group nor an expiring mask ever matches it. Copy it into #hzSafeG before each mask of the group
# (L.hz_opts(safe_g='cur')) and into mbHzSG of the group's safe markers; the module removes those markers itself.
scoreboard players remove #mbSafeN mb 1
execute unless score #mbSafeN mb matches -999999..-1 run scoreboard players set #mbSafeN mb -1
scoreboard players operation #mbSafeG mb = #mbSafeN mb
