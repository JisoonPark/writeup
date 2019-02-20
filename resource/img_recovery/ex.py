import Image

background = Image.open("0_pattern.png")
overlay = Image.open("1_pattern.png")

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

new_img = Image.blend(background, overlay, 0.5)
new_img.save("result.png","PNG")
