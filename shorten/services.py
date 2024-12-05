import qrcode
import io


def generate_qr(url: str):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")

    # seek(0) indica colocar el buffer al inicio
    img_byte_arr.seek(0)

    return img_byte_arr
