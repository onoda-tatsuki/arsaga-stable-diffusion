class BaseMessage:
    # エラーメッセージの基底クラス

    detail: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:

    # chatGPTからのレスポンスがない時
    class CHATGPT_NOT_RESPONSE(BaseMessage):
        detail = "ChatGPTからの応答がありません"

    # Stability AI APIでエラーが発生した場合
    class STABLE_DIFFUSION_GENERATE_FAILED:
        detail = "画像の生成に失敗しました"
