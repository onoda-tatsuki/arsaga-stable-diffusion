# ARSAGA_STABLE_DIFFUSION
chatGPT + Stable Diffusionを使用した画像生成用のpythonモジュール

## 動作環境
- Python: ^3.11
- langchain: ^0.1.12
- openai = "^1.14.0"

ライブラリの詳細はpyproject.tomlを確認してください。
LLM周りはアップデートが激しいので依存関係に注意してください。

# インストール
このリポジトリのurlを指定してpip, poetry等でインストールしてください。
インストール例
```text
[tool.poetry.dependencies]
arsaga-stable-diffusion = {git = "https://github.com/...url...", branch = "お好きなブランチ"}
```

## 構成
```text
.
├── README.md
├── arsaga_stable_diffusion // ライブラリの本体
│   ├── __init__.py
│   ├── errors // ライブラリで発生するエラーを定義したディレクトリ
│   │   ├── __init__.py
│   │   ├── error_message.py
│   │   └── exceptions.py
│   ├── openai // LLMを使用するクラスを定義したディレクトリ
│   │   ├── __init__.py
│   │   └── prompt_generator.py
│   ├── prompt // ライブラリ内で使用するプロンプトのテンプレート
│   │   ├── __init__.py
│   │   └── template.py
│   ├── schemas // 変数や返値の定義したディレクトリ
│   │   ├── __init__.py
│   │   ├── image.py
│   │   └── types.py
│   └── stable_diffusion // Stable Diffusionを使用するクラスを定義したディレクトリ
│       ├── __init__.py
│       ├── base.py
│       └── image_generator.py
├── makefile
├── poetry.lock
├── pyproject.toml
├── pyrightconfig.json // pyrightの設定ファイル
└── tests // テストコードのディレクトリ
    ...省略
```

## 使用方法
基本的にプロンプト(自然言語)を受け取り、画像のバイナリ(bytesクラス)を返すことを想定しています。
LLMを使用したクラスがプロンプトを受け取り、文字列(str | Coroutine[str])を返します。
画像生成を行うクラスが何かしらの入力を受け取って画像バイナリを返します。
それぞれのクラスは別々に使用することも可能です。

```python
# LLMのクラスインスタンスを作成


```