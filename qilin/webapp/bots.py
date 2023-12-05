from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from qilin.utils.crypto import encrypt_string
from pydantic import BaseModel


class Bot(BaseModel):
    name: str
    bot_type: str
    endpoint: str
    model: str
    api_version: str
    api_key: str


def create_bots_router():
    rt = APIRouter(prefix='/api')

    @rt.get('/bots/<bot_id>')
    async def get_bot(bot_id):
        file_path = f'bots/{bot_id}/bot.json'
        from qilin.webapp.appconfig import storage
        bot = await storage.read_json(file_path, Bot)
        bot.api_key = None
        return JSONResponse(bot.model_dump())
    
    
    @rt.post('/bots/<bot_id>')
    async def update_bot(bot_id: str, bot: Bot):
        bot.api_key = encrypt_string(bot.api_key)
        file_path = f'bots/{bot_id}/bot.json'
        from qilin.webapp.appconfig import storage
        await storage.save_json(file_path, bot)
        return Response(status=200)


    return rt