from uuid import UUID, uuid4


class RoomService:
    @classmethod
    async def create_room(cls) -> UUID:
        """
        Create room and return it's id
        """
        return uuid4()
    
    

