from typing import Literal, Union

gpt_type = Literal["gpt-4", "gpt-3.5-turbo"]

generator_type = Literal["v2"]

image_format = Literal["jpeg", "png", "webp"]

encoded_bytes = Union[bytes, str]

image_aspect = Literal[
    "21:9", "16:9", "5:4", "3:2", "1:1", "2:3", "4:5", "9:16", "9:21"
]
