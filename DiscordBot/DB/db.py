import aiosqlite
from DiscordBot.DB.UserTimezone import UserTimezone


class UserTimezoneDB:
    def __init__(self):
        self.db_name = "csbot.db"

    async def set_up_db(self):
        db = await aiosqlite.connect(self.db_name)
        await db.execute("CREATE TABLE IF NOT EXISTS user_timezones (id TEXT PRIMARY KEY, timezone TEXT)")
        await db.commit()
        await db.close()

    async def get_by_id(self, user_id: str) -> UserTimezone:
        db = await aiosqlite.connect(self.db_name)
        cursor = await db.execute(f"SELECT * FROM user_timezones WHERE id = '{user_id}'")
        found_row = await cursor.fetchone()
        await db.close()
        if found_row is None:
            return None
        user_id, timezone = found_row
        return UserTimezone(user_id, timezone)

    async def _insert(self, user_id: str, timezone: str) -> UserTimezone:
        db = await aiosqlite.connect(self.db_name)
        await db.execute(f"INSERT INTO user_timezones VALUES ('{user_id}', '{timezone}')")
        await db.commit()
        await db.close()
        return await self.get_by_id(user_id)

    async def _update_by_id(self, user_id: str, timezone: str) -> UserTimezone:
        db = await aiosqlite.connect(self.db_name)
        await db.execute(f"UPDATE user_timezones SET timezone = '{timezone}' WHERE id = '{user_id}'")
        await db.commit()
        await db.close()
        return await self.get_by_id(user_id)

    async def upsert(self, user_id: str, timezone: str) -> UserTimezone:
        found_row = await self.get_by_id(user_id)
        if found_row is None:
            return await self._insert(user_id, timezone)
        else:
            return await self._update_by_id(user_id, timezone)

    async def get_user_timezone_or_default(self, user_id: str):
        user_timezone = await self.get_by_id(user_id)
        if user_timezone is not None:
            return user_timezone.timezone
        else:
            return "America/Phoenix"
