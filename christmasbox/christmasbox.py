from iconservice import *

TAG = 'ChristmasBox'

class ChristmasBox(IconScoreBase):

    _DEAD_LINE = 'dead_line'
    _BOX_STATUS = 'box_status'
    _WINNER_LIST = 'winner_list'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._dead_line = VarDB(self._DEAD_LINE, db, value_type=int)
        self._box_status = DictDB(self._BOX_STATUS, db, value_type=int)
        self._winner_list = DictDB(self._WINNER_LIST, db, value_type=str)

    def on_install(self) -> None:
        super().on_install()
        self._box_status['box1'] = 0
        self._box_status['box2'] = 0
        self._box_status['box3'] = 0

    def on_update(self) -> None:
        super().on_update()
    

    @payable
    def fallback(self) -> None:
        amount = self.msg.value

        if amount == 1 * 10 ** 18:
            if self._box_status['box1'] == 1:
                revert(f"box1 apply is closed. winner is {self._winner_list['box1']}")
            else:
                win = int.from_bytes(sha3_256(self.msg.sender.to_bytes() + str(self.block.timestamp).encode()), "big") % 2
                if win == 0:
                    self._box_status['box1'] = 1
                    self._winner_list['box1'] = str(self.msg.sender)

        elif amount == 2 * 10 ** 18:
            if self._box_status['box2'] == 1:
                revert(f"box2 apply is closed. winner is {self._winner_list['box2']}")
            else:
                win = int.from_bytes(sha3_256(self.msg.sender.to_bytes() + str(self.block.timestamp).encode()), "big") % 4
                if win == 0:
                    self._box_status['box2'] = 1
                    self._winner_list['box2'] = str(self.msg.sender)
             

        elif amount == 4 * 10 ** 18:
            if self._box_status['box3'] == 1:
                revert(f"box3 apply is closed. winner is {self._winner_list['box3']}")
            else:
                win = int.from_bytes(sha3_256(self.msg.sender.to_bytes() + str(self.block.timestamp).encode()), "big") % 8
                if win == 0:
                    self._box_status['box3'] = 1
                    self._winner_list['box3'] = str(self.msg.sender)
             
        else:
            revert(f"please send 1 or 2 or 4 ICX for apply")

        # do the flip.
        if win == 0:
            Logger.debug(f'Winner! {self.msg.sender}.', TAG)
        else:
            Logger.debug(f'Apply Fail.', TAG)

    @external(readonly=True)
    def help(self) -> str:
        return "Required ICX for each present. Present1 : 1 ICX. Present2 : 2 ICX. Present3 : 4 ICX"

    @external(readonly=True)
    def get_winnerlist(self) -> dict:
        winner_result = {}
        winner_result['box1'] = self._winner_list['box1']
        winner_result['box2'] = self._winner_list['box2']
        winner_result['box3'] = self._winner_list['box3']
        if self._box_status['box1'] == 0:
            winner_result['box1'] = "No Winner"
        if self._box_status['box2'] == 0:
            winner_result['box2'] = "No Winner"
        if self._box_status['box3'] == 0:
            winner_result['box3'] = "No Winner"    
        return winner_result
