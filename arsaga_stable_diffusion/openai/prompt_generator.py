from __future__ import annotations

import os
from typing import Optional

from langchain.callbacks.manager import get_openai_callback
from langchain.globals import set_debug, set_verbose
from langchain_community.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_core.pydantic_v1 import SecretStr
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from prompt.template import OpenAIPromptTemplate
from stable_diffusion.image_generator import V2ImageGenerator

if os.environ["LANGCHAIN_DEBUG_MODE"] == "ALL":
    set_debug(True)
elif os.environ["LANGCHAIN_DEBUG_MODE"] == "VERBOSE":
    set_verbose(True)


class PromptGenerator:
    # todo 引数に型定義をする
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0,
        verbose: bool = False,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("OPENAI_AI_API_KEY")

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
        sd_designer_prompt_template: str = OpenAIPromptTemplate.SD_DESIGN_TEMPLATE,
        sd_maker_prompt_template: str = OpenAIPromptTemplate.SD_PROMPT_TEMPLATE,
    ) -> tuple[str, OpenAICallbackHandler]:
        sd_design_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(sd_designer_prompt_template),
                ("human", "{human_input}"),
            ]
        )

        sd_prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(sd_maker_prompt_template),
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

    def bind_image_generator(self) -> None:
        self.generator = V2ImageGenerator()
