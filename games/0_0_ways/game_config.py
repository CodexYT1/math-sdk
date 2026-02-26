"""Ways game configuration - FIXED 97% RTP"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode

class GameConfig(Config):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_ways"
        self.provider_number = 0
        self.working_name = "Production Ways Slot"
        self.wincap = 5000.0
        self.win_type = "ways"
        self.rtp = 0.9700
        self.construct_paths()

        # Standard 5x3-4 ways slot
        self.num_reels = 5
        self.num_rows = [3, 3, 3, 3, 3]

        # FIXED PAYTABLE - Conservative 97% RTP
        pay_group = {
            # High pays
            (3, "H1"): 10.0,
            (4, "H1"): 50.0,
            (5, "H1"): 200.0,
            (3, "H2"): 5.0,
            (4, "H2"): 25.0,
            (5, "H2"): 100.0,
            (3, "H3"): 2.5,
            (4, "H3"): 12.0,
            (5, "H3"): 50.0,
            # Low pays  
            (3, "L1"): 0.8,
            (4, "L1"): 4.0,
            (5, "L1"): 20.0,
            (3, "L2"): 0.6,
            (4, "L2"): 3.0,
            (5, "L2"): 15.0,
            (3, "L3"): 0.4,
            (4, "L3"): 2.0,
            (5, "L3"): 10.0,
        }
        self.paytable = self.convert_range_table(pay_group)

        self.special_symbols = {"wild": ["W"], "scatter": ["S"]}
        
        # TIGHTER BONUS - 3+ scatters only
        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 15, 5: 20},
            self.freegame_type: {3: 5, 4: 8},
        }

        self.maximum_board_mult = 256

        # Standard reel strips
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))
        
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=5000,
                distributions=[
                    Distribution(criteria="wincap", quota=0.0005, win_criteria=5000, conditions={"force_wincap": True}),
                    Distribution(criteria="freegame", quota=0.08, conditions={"force_freegame": True}),
                    Distribution(criteria="0", quota=0.45, win_criteria=0.0),
                    Distribution(criteria="basegame", quota=0.47),
                ],
            ),
            BetMode(
                name="bonus", 
                cost=100,
                rtp=self.rtp,
                max_win=5000,
                distributions=[
                    Distribution(criteria="wincap", quota=0.001, win_criteria=5000, conditions={"force_wincap": True}),
                    Distribution(criteria="freegame", quota=0.1, conditions={"force_freegame": True}),
                ],
            ),
        ]
