import base64

from pydantic import BaseModel, ConfigDict, Field

from arsaga_stable_diffusion.schemas.types import encoded_bytes


class ImageResponse(BaseModel):
    b64_bytes: encoded_bytes = Field(min_length=1)
    reversed_prompt: str = Field(min_length=1)
    total_tokens: int = Field(ge=1)

    model_config = ConfigDict(
        extra="forbid",  # 追加の属性を拒否する
        frozen=True,  # 値の変更を拒否する
    )

    def decode_b64_bytes(self) -> bytes:
        return base64.b64decode(self.b64_bytes)
