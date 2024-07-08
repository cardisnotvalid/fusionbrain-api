from typing import Union
import base64


def save_image_b64(image: Union[str, bytes], filepath: str) -> None:
    image_data = image.encode() if isinstance(image, str) else image
    b64_data = base64.b64decode(image_data)
    try:
        with open(filepath, "wb") as f:
            f.write(b64_data)
        print(f"The image is saved to `{filepath}`")
    except Exception as err:
        print(f"Failed to save image. {err}")
