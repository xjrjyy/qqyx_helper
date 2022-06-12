class IdGenerator:
    _id_counter: int

    def __init__(self) -> None:
        self._id_counter = 0
    
    def generate_id(self) -> int:
        self._id_counter += 1
        return self._id_counter