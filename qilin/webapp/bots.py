from flask import Blueprint, jsonify, request, Response
from qilin.webapp.appconfig import storage
from qilin.utils.jsondata import json_loads
from qilin.utils.crypto import encrypt_string
from dataclasses import dataclass, asdict


@dataclass
class Bot:
    name: str
    bot_type: str
    endpoint: str
    model: str
    api_version: str
    api_key: str


def create_bots_blueprint():
    bp = Blueprint('bots', __name__)

    @bp.route('/bots/<bot_id>', methods=['GET'])
    async def get_bot(bot_id):
        file_path = f'bots/{bot_id}/bot.json'
        bot = await storage.read_json(file_path, Bot)
        bot.api_key = None
        return jsonify(asdict(bot))
    
    
    @bp.route('/bots/<bot_id>', methods=['POST'])
    async def update_bot(bot_id):
        json_str = request.get_data(as_text=True)
        bot = json_loads(Bot, json_str)
        bot.api_key = encrypt_string(bot.api_key)
        file_path = f'bots/{bot_id}/bot.json'
        await storage.save_json(file_path, bot)
        return Response(status=200)


    return bp