class BaseMessage:
    # エラーメッセージの基底クラス

    text: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:

    # chatGPTからのレスポンスがない時
    class CHATGPT_NOT_RESPONSE(BaseMessage):
        text = "ChatGPTからの応答がありません"
