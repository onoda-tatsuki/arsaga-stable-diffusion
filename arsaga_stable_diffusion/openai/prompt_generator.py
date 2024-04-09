from __future__ import annotations

import os
from typing import Optional

from langchain.callbacks.manager import get_openai_callback
from langchain.globals import set_debug, set_verbose
from langchain_community.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate  # fmt: on
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.pydantic_v1 import SecretStr
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from arsaga_stable_diffusion.prompt.template import OpenAIPromptTemplate
from arsaga_stable_diffusion.schemas.image import ImageResponse
from arsaga_stable_diffusion.schemas.types import generator_type, gpt_type
from arsaga_stable_diffusion.stable_diffusion.base import ImageGeneratorFactory

if os.getenv("LANGCHAIN_DEBUG_MODE") == "ALL":
    set_debug(True)
elif os.getenv("LANGCHAIN_DEBUG_MODE") == "VERBOSE":
    set_verbose(True)


class PromptGenerator:
    # todo 引数に型定義をする
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: gpt_type = "gpt-3.5-turbo",
        temperature: float = 0,
        verbose: bool = False,
    ) -> None:
        if api_key is None:
            api_key = os.getenv("OPENAI_AI_API_KEY")

        if api_key is None:
            raise ValueError("Missing OpenAI API Key")

        self.api_key = api_key
        self.generator = None

        self.lim = ChatOpenAI(
            model=model,
            api_key=SecretStr(self.api_key),
            temperature=temperature,
            verbose=verbose,
        )

    def _make_sd_prompt(
        self,
        prompt: str,
        designer_template: Optional[str] = None,
        prompt_maker_template: Optional[str] = None,
    ) -> tuple[str, OpenAICallbackHandler]:
        sd_design_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    designer_template or OpenAIPromptTemplate.SD_DESIGN_TEMPLATE
                ),
                ("human", "{human_input}"),
            ]
        )

        sd_prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    prompt_maker_template or OpenAIPromptTemplate.SD_PROMPT_TEMPLATE
                ),
                ("human", "{human_input}"),
            ]
        )

        output_parser = StrOutputParser()

        chain = (
            {
                "ai_input": sd_design_template | self.lim | output_parser,
                "human_input": RunnablePassthrough(),
            }
            | sd_prompt_template
            | self.lim
            | output_parser
        )

        with get_openai_callback() as callback:
            response = chain.invoke({"human_input": prompt})

        # todo 返り値をどうするか検討する
        return response, callback

    def bind_image_generator(
        self,
        generator_type: generator_type = "v2",
        api_key: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.generator = ImageGeneratorFactory.create(generator_type, api_key, **kwargs)

    def make_image_by_prompt(
        self,
        prompt: str,
        designer_template: Optional[str],
        prompt_maker_template: Optional[str],
    ):
        if self.generator is None:
            # todo エラーの型定義を行う
            raise Exception("Image Generator class not initialized")

        response, token_info = self._make_sd_prompt(
            prompt, designer_template, prompt_maker_template
        )

        image = self.generator.generate_image(response)

        return ImageResponse(
            b64_bytes=image,
            reversed_prompt=response,
            total_tokens=token_info.total_tokens,
        )
