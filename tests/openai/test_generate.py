from arsaga_stable_diffusion.openai.prompt_generator import PromptGenerator

class TestPromptGenerator:
    def test_make_image_success(self) -> None:

        generator = PromptGenerator()
        generator.bind_image_generator()
        image = generator.make_image_by_prompt(prompt="歴戦の傭兵", image_format="png")
        
        assert isinstance(image.decode_b64_bytes(), bytes)
        assert len(image.decode_b64_bytes()) > 0
        
        # pngファイルかどうか確認
        expected_signature = bytes([137, 80, 78, 71, 13, 10, 26, 10])
        assert image.decode_b64_bytes().startswith(expected_signature)