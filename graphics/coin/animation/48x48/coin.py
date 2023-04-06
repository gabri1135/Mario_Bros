from PIL import Image

for i in range(0,9):
    img=Image.open(f'48x48/{i}.png')
    print(img.mode)
    new_img=Image.new('RGBA',(48,48),(0, 0, 0, 0))
    x,y=img.size
    new_x=int(x/y*36)
    new_x-=new_x%2
    image_res=img.resize((new_x,36))
    new_img.paste(image_res,((48-new_x)//2,6))
    new_img.save(f'{i}.png')

'''
print(img.mode)
new_img=Image.new('RGBA',(48,48),(0, 0, 0, 0))
x,y=img.size
new_x=int(x/y*48)
new_x-=new_x%2
image_res=img.resize((new_x,48))
new_img.paste(image_res,((48-new_x)//2,0))
'''