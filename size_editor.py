from PIL import Image
img = Image.open('Save-icon.png')
new_img = img.resize((40,40))
new_img.save('guardado.png','png')