# Put-away clip "sheathe" (Skirk). char/motion/sheath/begin starts it when the drawn delay runs out while idle
# on the ground; until clips.sheathe exists in tools/player_motion/skirk.json the quick stow is used instead.
# No gameplay events (no movement lock: attacks and movement cancel it). If audio_skirk.py returns layers for
# "sheathe", add the per-frame audio hook line for skirk/sheathe exactly once and rerun tools/build_player_audio.py.
