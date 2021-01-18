from collections.abc import Sequence
from .typings.base_command import BaseCommand
from typing import Any, Coroutine, Optional

from khl.Bot import Bot
from .typings import BaseSession, SessionResult, ResultType
from khl.Message import Msg


class Session(BaseSession):
    command: BaseCommand
    command_str: str
    args: Sequence[str]
    msg: Msg
    bot: Bot

    def __init__(self,
                 command: BaseCommand,
                 command_str: str,
                 args: Sequence[str],
                 msg: Msg,
                 bot: Optional[Bot] = None) -> None:
        super().__init__(command=command,
                         command_str=command_str,
                         args=args,
                         msg=msg,
                         bot=bot)

    def reply(
        self,
        content: str,
        result_type: ResultType = ResultType.SUCCESS
    ) -> Coroutine[Any, Any, SessionResult]:
        func_result = self.send(content=content,
                                result_type=result_type,
                                mention=True,
                                reply=True)
        return func_result

    def reply_only(
        self,
        content: str,
        result_type: ResultType = ResultType.SUCCESS
    ) -> Coroutine[Any, Any, SessionResult]:
        func_result = self.send(content=content,
                                result_type=result_type,
                                mention=False,
                                reply=True)
        return func_result

    def mention(
        self,
        content: str,
        result_type: ResultType = ResultType.SUCCESS
    ) -> Coroutine[Any, Any, SessionResult]:
        func_result = self.send(content=content,
                                result_type=result_type,
                                mention=True,
                                reply=False)
        return func_result

    async def send(self,
                   content: str,
                   result_type: ResultType = ResultType.SUCCESS,
                   message_type: Msg.Types = Msg.Types.KMD,
                   mention: bool = False,
                   reply: bool = False) -> SessionResult:

        if (mention):
            content = f'(met){self.msg.author_id}(met) ' + content
        quote: str = self.msg.msg_id if (reply) else ''

        if (not self.bot):
            raise AttributeError('Session send used before assigning a bot.'
                                 f' Command: {self.command.name}')
        msg_sent = self.bot.send(object_name=message_type,
                                 content=content,
                                 channel_id=self.msg.target_id,
                                 quote=quote)
        return SessionResult(result_type=result_type,
                             session=self,
                             msg_sent=msg_sent)
